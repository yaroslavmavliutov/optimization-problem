import subprocess
import os
import csv
import matplotlib.pyplot as plt
import numpy as np

nrun = 20
filename = 'result'
threshold = 475.0

# for r in range(nrun):
#     os.system("python snp.py -n 2 -s 42 -run " + str(r))

result_global = []
for i in range(nrun):
    result_global.append([])
    with open(filename + str(i) + '.csv', 'r') as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            result_global[-1].append(row[0])

distribution = []
current_max = [0.0]*nrun
for j in range(len(max(result_global, key=len))):
    success = 0
    for i in range(nrun):
        try:
            if float(result_global[i][j]) > current_max[i]:
                current_max[i] = float(result_global[i][j])
                value = float(result_global[i][j])
            else:
                value = current_max[i]
        except:
            value = current_max[i]

        if value >= threshold:
            success = success + 1
    distribution.append(success/nrun)

print(distribution)

x = np.arange(1, 8)
y = np.random.randint(1, 20, size = 7)

fig, ax = plt.subplots()

ax.bar(range(len(distribution)), np.asarray(distribution))

ax.set_facecolor('seashell')
fig.set_facecolor('floralwhite')
fig.set_figwidth(12)    #  ширина Figure
fig.set_figheight(6)    #  высота Figure

plt.show()

# Подумати за цей рандом сід. Як його встановити правильно
# З папками розібратись, шоб зберігали результати в папку
# шоб передавались всі правильні параметри з строку термінала через пайтон