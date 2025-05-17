# -*- coding: utf-8 -*-

import subprocess

# input correct paths (output__file-results; script path-directory of second script; python_exe-location of python)
output_file_path = r'C:\Users\krzys\OneDrive\Pulpit\MKWS\results.txt'
python_exe = r'C:\Users\krzys\AppData\Local\Microsoft\WindowsApps\python.exe'
script_path = r'C:\Users\krzys\OneDrive\Pulpit\MKWS\postprocess.py'

#results file clear
with open(output_file_path, 'w') as file:
    file.write('')

analysis = Model.Analyses[0]
mesh = Model.Mesh
mesh.GenerateMesh()
solution = analysis.Solution

# adding fixed constraint
fixed_support = analysis.AddFixedSupport()
fixed_support.Location = ExtAPI.DataModel.GetObjectsByName("fixed")[0]

# list of loads
load_cases = [
    {"type": "force", "name": "load", "value": -10000},   # N
    {"type": "pressure", "name": "load", "value": -100},    # MPa
    {"type": "moment", "name": "load", "value": 1000}     # N·m
]


# adding solutions
eq_stress = solution.AddEquivalentStress()
deformation = solution.AddTotalDeformation()

# main loop
for idx, case in enumerate(load_cases):
   
    # deleting previous load
    to_delete = []
    for obj in analysis.Children:
        typename = str(type(obj))
        if "Force" in typename or "Pressure" in typename or "Moment" in typename or "Result" in typename:
            to_delete.append(obj)
    for obj in to_delete:
        obj.Delete()

    # adding load
    load = None
    target = ExtAPI.DataModel.GetObjectsByName(case["name"])[0]

    if case["type"] == "force":
        load = analysis.AddForce()
        load.Location = target
        load.DefineBy = LoadDefineBy.Components
        load.YComponent.Output.SetDiscreteValue(0, Quantity(case["value"], "N"))

    elif case["type"] == "pressure":
        load = analysis.AddPressure()
        load.Location = target
        load.Magnitude.Output.SetDiscreteValue(0, Quantity(case["value"], "MPa"))

    elif case["type"] == "moment":
        load = analysis.AddMoment()
        load.Location = target
        load.DefineBy = LoadDefineBy.Components
        load.ZComponent.Output.SetDiscreteValue(0, Quantity(case["value"], "N m"))

    # clear previous data and solve
    solution.ClearGeneratedData()
    solution.Solve()

    max_stress = float(eq_stress.Maximum.Value)
    max_deformation = float(deformation.Maximum.Value)

    # saving to file
    with open(output_file_path, 'a') as file:
        #file.write("Typ obciazenia: {}\n".format(case["type"]))
        file.write("{:.2f}\t".format(max_stress))
        file.write("{:.2f}\n".format(max_deformation))


# second script call
subprocess.Popen([python_exe, script_path])


