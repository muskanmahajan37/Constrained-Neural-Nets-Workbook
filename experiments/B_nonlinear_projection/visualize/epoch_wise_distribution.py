"""Tools for plotting complete distributions for each object"""

import matplotlib.pyplot as plt
import numpy as np

from .config import DEFAULT_DIRECTORY
from .readability_utils import _clean_label, _correct_and_clean_labels
from .retrieval_utils import retrieve_object


__all__ = ["plot_epoch_wise_distribution"]


def plot_epoch_wise_distribution(
    xvalues,
    yvalues,
    labels,
    savefile,
    colors=None,
    title="Untitled",
    xlabel="Epoch",
    ylabel="Unspecified",
    log=False,
    directory=DEFAULT_DIRECTORY,
):
    """Plots a distribution with several curves for each monitor for the given 
    object string

    :param xvalues: a list of lists. Probably [x.epoch for x in monitors]
    :param yvalues: a list of 2d numpy arrays, where the first dimension is by
        epochs and the second is different percentiles
    :param labels: a list of strings for the label of each monitor
    :param savefile: name of the file to save. If none, then will not save
    :param colors: a list of colors or None. If a sorted list of integers is 
        given, then it is interpreted as identities for colors
    :param title: title of the figure. Defaults to "Untitled"
    :param ylabel: label for the y-axis. Defaults to "Unspecified"
    :param xlabel: label for the x-axis. Defaults to "Epoch"
    :param log: whether to plot a log-plot. Can also be set to "symlog"
    :param directory: directory to save the file in. Defaults to the results dir
    :returns: the figure
    """
    stashed_colors = list()
    if colors is None:
        colors = [None for _ in labels]
    clean_labels = _correct_and_clean_labels(labels)

    fig = plt.figure()
    for xvalue, yvalue, label, color in zip(
        xvalues, yvalues, clean_labels, colors
    ):
        percentiles = np.array(yvalue)
        xvalue = np.array(xvalue)
        midpoint = int((percentiles.shape[1] - 1) / 2)
        if color is None:
            line2d = plt.plot(
                xvalue, percentiles[:, midpoint], "-", label=label, zorder=10
            )
            color = line2d[0].get_color()
        elif isinstance(color, int):
            if len(stashed_colors) > color:
                color = stashed_colors[color]
                plt.plot(
                    xvalue,
                    percentiles[:, midpoint],
                    "-",
                    label=label,
                    color=color,
                    zorder=10,
                )
            else:
                line2d = plt.plot(
                    xvalue,
                    percentiles[:, midpoint],
                    "-",
                    label=label,
                    zorder=10,
                )
                color = line2d[0].get_color()
                stashed_colors.append(color)
        else:
            plt.plot(
                xvalue,
                percentiles[:, midpoint],
                "-",
                label=label,
                color=color,
                zorder=10,
            )

        for i in range(midpoint):
            plt.fill_between(
                xvalue,
                percentiles[:, i],
                percentiles[:, -i - 1],
                color=color,
                alpha=(
                    5.0 / (percentiles.shape[1] - 1)
                ),  # This requires >5 percentiles!
                zorder=0,
            )
        plt.plot(xvalue, percentiles[:, 0], ":", color=color, zorder=10)
        plt.plot(xvalue, percentiles[:, -1], ":", color=color, zorder=10)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    l = plt.legend()
    l.set_zorder(20)

    # possibly make log plot
    if log:
        if log == "symlog":
            plt.yscale("symlog")
        else:
            plt.yscale("log")

    plt.tight_layout()

    if savefile is not None:
        filepath = f"{directory}/{savefile}.png"
        print(f"Saving {title} distribution plot to {filepath}")
        plt.savefig(filepath, dpi=300)
    return fig
