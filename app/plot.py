import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def plot(solutions):
    def get_points(solutions):
        points = pd.DataFrame(solutions)
        return points, points.shape[1]

    def two_dim(solutions, label, axis_labels):
        n = int(np.ceil(np.sqrt(1)))
        fig = plt.figure()
        fig.suptitle('Pareto front approximation', fontsize=16)

        points, _ = get_points(solutions)

        ax = fig.add_subplot(n, n, 1)
        points.plot(kind='scatter', x=0, y=1, ax=ax, s=10, color='#236FA4', alpha=1.0)

        if label:
            ax.set_title(label)

        if axis_labels:
            plt.xlabel(axis_labels[0])
            plt.ylabel(axis_labels[1])

        plt.savefig('NRP_result.png', format='png', dpi=200)

        plt.close(fig=fig)

    axis_labels = ['profit', 'cost']
    # label = method + '-NRP'
    label = 'NRP'
    two_dim(solutions, label, axis_labels)
