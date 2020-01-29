import os
import csv
import matplotlib.pyplot as plt
import numpy as np
import timeit
import os.path as op


def find_optimal(nrun=1, execute="python snp.py -n 2"):
    for r in range(nrun):
        os.system(execute + " -run " + str(r) + " -s " + str(r))

def create_distribution(nrun, threshold, filename):
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
    return distribution

def lineplot(ax, x_data, y_data, color, algo):
    ax.plot(x_data, y_data, lw = 2, color = color, alpha = 1, label=algo)
    ax.legend([algo])

# def parsing():
#
#     can = argparse.ArgumentParser()
#     can.add_argument("-f", "--fname", metavar="NAME", default="file_result_runs",
#                      help="Name of result files")

def main():
    nrun = 20
    solvers = ["genetic", "num_random", "num_greedy"] #,"bit_greedy", "sa"]
    threshold = 495.0
    distribution = dict()

    for selected in solvers:
        result_dir = "2sensors_result_" + selected
        #result_dir = "result_" + selected
        fname = "result"
        filepath = op.join(result_dir, fname)

        if op.isdir(result_dir): pass
        else: os.mkdir(result_dir)

        start = timeit.default_timer()
        if selected == "genetic":
            exec = "python snp.py -n 2 -m " + selected + " -f " + filepath
        else:
            exec = "python snp.py -n 2 -m " + selected + " -f " + filepath + " -i " + \
                   str(len(distribution["genetic"])) + " -y " + str(len(distribution["genetic"]))
            # exec = "python snp.py -n 3 -m " + selected + " -f " + filepath

        #find_optimal(nrun=nrun, execute=exec)
        stop_algo = timeit.default_timer()
        distribution[selected] = create_distribution(nrun=nrun, threshold=threshold, filename=filepath)
        stop_dist = timeit.default_timer()
        print("----------------", selected)
        print('Time to find the optimal value: ', stop_algo - start)
        print('Time to calculate the distribution: ', stop_dist - stop_algo)
        print('Total Time: ', stop_dist - start)

    _, ax = plt.subplots()
    ax.set_title("Comparison of probabilities with threshold=" + str(threshold))
    ax.set_xlabel("#func")
    ax.set_ylabel("proba")
    lineplot(ax, range(len(distribution["genetic"])), np.asarray(distribution["genetic"]), color="red", algo = "genetic")
    lineplot(ax, range(len(distribution["num_greedy"])), np.asarray(distribution["num_greedy"]), color="blue", algo = "num_greedy")
    lineplot(ax, range(len(distribution["num_random"])), np.asarray(distribution["num_random"]), color="black", algo="num_random")
    ax.legend()
    plt.show()


if __name__ == '__main__':
    main()

# Подумати за цей рандом сід. Як його встановити правильно
# З папками розібратись, шоб зберігали результати в папку +++++++++++++++++++++++++++++++
# шоб передавались всі правильні параметри з строку термінала через пайтон +++++++++++
# шоб схрещення було і на 3 каптора, і на 4 +++++++++++++++++++++++++++
# дослідження області при генерації популяції
# яка різниця між визначення функції bit i num. Для нас яку юзати?
# другий алгоритм recuit simule
# кількість ітерацій в гріді і генетичному (штучно збільшуємо)
# рандом і гріді
# рандом сід
# mavliutov.zip