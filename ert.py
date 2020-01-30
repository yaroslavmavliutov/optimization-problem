import os
import csv
import matplotlib.pyplot as plt
import numpy as np
import timeit
import os.path as op


def find_optimal(nrun=1, execute="python snp.py -n 2"):
    for r in range(nrun):
        # to set the run's number and random.seed. In this case, these are the same values
        os.system(execute + " -run " + str(r) + " -s " + str(r))

def create_distribution(nrun, threshold, filename):
    result_global = []
    for i in range(nrun):
        result_global.append([])
        # .csv files parsing
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


def main():
    nrun = 20
    solvers = ["genetic", "num_random", "num_greedy"]
    threshold = 830.0
    nsensors = 4

    distribution = dict()

    for selected in solvers:
        result_dir = str(nsensors) + "sensors_result_" + selected
        #result_dir = "result_" + selected
        fname = "result"
        filepath = op.join(result_dir, fname)

        if op.isdir(result_dir): pass
        else: os.mkdir(result_dir)

        start = timeit.default_timer()
        if selected == "genetic":
            exec = "python snp.py -n " + str(nsensors) + " -m " + selected + " -f " + filepath
        else:

            # in order to make the results of the algorithms comparable we artificially increase the number of iterations
            if "genetic" in distribution.keys():
                exec = "python snp.py -n " + str(nsensors) + " -m " + selected + " -f " + filepath + " -i " + \
                       str(len(distribution["genetic"])) + " -y " + str(len(distribution["genetic"]))
            else: exec = "python snp.py -n " + str(nsensors) + " -m " + selected + " -f " + filepath

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


# дослідження області при генерації популяції
# mavliutov.zip