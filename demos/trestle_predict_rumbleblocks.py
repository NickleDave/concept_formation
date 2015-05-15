import json
import numpy as np
import matplotlib.pyplot as plt

from utils import lowess
from utils import mean_confidence_interval
from predict import incremental_prediction
from trestle import TrestleTree
from dummy import DummyTree

num_runs = 30
num_examples = 50

with open('data_files/rb_s_07_continuous.json') as fin:
    towers = json.load(fin)

############################## GENERATE PREDICTIONS ##########################

naive_accuracy = incremental_prediction(DummyTree(), towers,
                                  run_length=num_examples,
                                  runs=num_runs, attr="success")
cobweb_accuracy = incremental_prediction(TrestleTree(), towers,
                                  run_length=num_examples,
                                  runs=num_runs, attr="success")

############################## PLOT RESULTS ##################################

cobweb_data = [[] for i in range(len(cobweb_accuracy[0]))]
naive_data = [[] for i in range(len(naive_accuracy[0]))]

for run in cobweb_accuracy:
    for i,v in enumerate(run):
        cobweb_data[i].append(v)
for run in naive_accuracy:
    for i,v in enumerate(run):
        naive_data[i].append(v)


cobweb_y = np.array([0] + [mean_confidence_interval(l)[0] for l in cobweb_data])
naive_y = np.array([0] + [mean_confidence_interval(l)[0] for l in naive_data])

x = np.array([i for i in range(len(cobweb_y))])

cobweb_y_smooth = lowess(x, cobweb_y)
naive_y_smooth = lowess(x, naive_y)

#x = np.array([1+i for i in range(len(cobweb_y_smooth))])

cobweb_lower = np.array([0] + [mean_confidence_interval(l)[1] for l in
                         cobweb_data])
naive_lower = np.array([0] + [mean_confidence_interval(l)[1] for l in
                        naive_data])

cobweb_lower_smooth = lowess(x, cobweb_lower)
naive_lower_smooth = lowess(x, naive_lower)

cobweb_upper = np.array([0] + [mean_confidence_interval(l)[2]
                         for l in cobweb_data])
naive_upper = np.array([0] + [mean_confidence_interval(l)[2]
                        for l in naive_data])

cobweb_upper_smooth = lowess(x, cobweb_upper)
naive_upper_smooth = lowess(x, naive_upper)

plt.fill_between(x, cobweb_lower_smooth, cobweb_upper_smooth, alpha=0.5,
                 facecolor="green")
plt.fill_between(x, naive_lower_smooth, naive_upper_smooth, alpha=0.5,
                 facecolor="red")

plt.plot(x, cobweb_y_smooth, label="TRESTLE", color="green")
plt.plot(x, naive_y_smooth, label="Naive Predictor", color="red")

plt.gca().set_ylim([0.00,1.0])
plt.gca().set_xlim([0,len(naive_y_smooth)-1])
plt.title("Incremental Tower Success Prediction Accuracy")
plt.xlabel("# of Training Examples")
plt.ylabel("Avg. Probability of True Success Label (Accuracy)")
plt.legend(loc=4)

plt.show()
