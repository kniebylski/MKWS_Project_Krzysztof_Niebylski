import matplotlib.pyplot as plt

# input correct directory of results file
input_file = r'C:\Users\krzys\OneDrive\Pulpit\MKWS\results.txt'

# reading data
case = ["Force", "Pressure", "Moment"]
stress = []
deformation = []

with open(input_file, 'r') as file:
    for linia in file:
        czesci = linia.strip().split('\t')  # Dzieli linię po tabulatorze
        if len(czesci) == 2:
            a, b = czesci
            stress.append(float(a))
            deformation.append(float(b))

print("x:", stress)
print("y:", deformation)

# graph settings
fig, ax1 = plt.subplots(figsize=(8, 6))

# position of bars
x_pos = range(len(stress))
bar_width = 0.35

# stress bars
bars1 = ax1.bar(x_pos, stress, bar_width, label="Stress", color='royalblue')
ax1.set_ylabel('Stress [MPa]', fontsize=12)
ax1.set_title('Analysis Results', fontsize=14)

# x axis labels
ax1.set_xticks([p + bar_width / 2 for p in x_pos])
ax1.set_xticklabels(case)

# y axis setup
ax2 = ax1.twinx()
bars2 = ax2.bar([p + bar_width for p in x_pos], deformation, bar_width, label="Deformation", color='darkorange')
ax2.set_ylabel('Deformation [mm]', fontsize=12)

# labels above bars (stress)
for bar in bars1:
    height = bar.get_height()
    ax1.annotate(f'{height:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 3), textcoords='offset points',
                 ha='center', va='bottom', fontsize=9)

# labels abve bars (deformation)
for bar in bars2:
    height = bar.get_height()
    ax2.annotate(f'{height:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 3), textcoords='offset points',
                 ha='center', va='bottom', fontsize=9)

# legend
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# chart saving
chart_path = r'C:\Users\krzys\OneDrive\Pulpit\MKWS\graph.png'
plt.savefig(chart_path)

# graph plotting
plt.show()
