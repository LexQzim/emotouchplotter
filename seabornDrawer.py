import os

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D
from matplotlib.collections import PatchCollection

import seaborn as sns

symbole_time = [6, 12, 21, 33, 42, 51, 57, 63]

sns.set_theme(style="whitegrid")

# prepare legend
patch_yellow_box = patches.Patch(
    color="#FFFF0055", edgecolor="#FFFF0055", label="Aufforderung"
)
patch_noise_plot = patches.Patch(
    color="#C0C0C055", edgecolor="#C0C0C055", label="Rauschkurve"
)
song_ends = Line2D(
    [0], [0], color="k", linestyle="dashed", label="Ende vom Liedausschnitt"
)
rating_origin = Line2D(
    [0],
    [0],
    marker="o",
    markersize=10,
    markerfacecolor="#00800055",
    linestyle="",
    label="Wertungen (original)",
)
rating_resampled_line = Line2D(
    [0], [0], color="#008000", linestyle="solid", label="Wertungen (resampled)"
)
rating_resampled_dot = Line2D(
    [0],
    [0],
    marker="o",
    markersize=10,
    markerfacecolor="#00800055",
    linestyle="",
    label="Wertungen (resampled)",
)


def _polynomial_function(p, x, power):
    result = 0
    for i in range(power):
        result += (x ** (power - i)) * p[i]
    return result


def _generate_noise_function(x, power=4, fadeIn=True):
    """
    Generates the noise function.
    This is just a mockup and doesn't really represents the current noise curve.
    Because it is not clear which exponential equation audacity is using for there fade in or fade out.
    But if want you can adjust the curve with power.
    My suggestion is power of 2 but visually it isn't that nice.
    """
    if fadeIn:
        y = [0, 0.8]
    else:
        y = [0.8, 0]

    # calculate parameter for polinomial function of given power
    p = np.polyfit(x, y, power)

    # calculate new values for fitted curve
    xf = np.linspace(x[0], x[1], 50)
    yf = _polynomial_function(p, xf, power)
    yf -= yf[0]

    if not fadeIn:
        yf = -np.flip(yf)

    polynomDf = pd.DataFrame(data={"x": xf, "y": yf})

    return xf, yf, polynomDf


def _draw_noise_function(noise_version):
    """
    Adds one of the two available noise functions to the current plot.
    """
    if noise_version == 0:
        return
    elif noise_version == 1:
        # version 1
        # fade in
        x = [11, 39]
        xf1, yf1, polynomDf = _generate_noise_function(x)
        # sns.lineplot(polynomDf, x="x", y="y")

        # fade out
        x = [39, 68]
        xf2, yf2, polynomDf = _generate_noise_function(x, fadeIn=False)
        # sns.lineplot(polynomDf, x="x", y="y")

        calculated_x_noise_values = xf1.tolist() + xf2.tolist()
        calculated_y_noise_values = yf1.tolist() + yf2.tolist()

    elif noise_version == 2:
        # version 2
        # quick fade in
        x = [0, 0.85]
        xf1, yf1, polynomDf = _generate_noise_function(x, power=2)
        # sns.lineplot(polynomDf, x="x", y="y")

        # fade out
        x = [0.85, 30]
        xf2, yf2, polynomDf = _generate_noise_function(x, fadeIn=False)
        # sns.lineplot(polynomDf, x="x", y="y")

        # fade in
        x = [37, 68]
        xf3, yf3, polynomDf = _generate_noise_function(x)
        yf3 = np.flip(yf2)
        # sns.lineplot(polynomDf, x="x", y="y")

        calculated_x_noise_values = xf1.tolist() + xf2.tolist() + xf3.tolist()
        calculated_y_noise_values = yf1.tolist() + yf2.tolist() + yf3.tolist()

    plt.fill_between(
        calculated_x_noise_values,
        calculated_y_noise_values,
        alpha=0.3,
        facecolor="silver",
    )


def _draw_signal_boxes(axes):
    """
    Add on given timing vertical yellow boxes to symbolize when the signal is shown
    """
    rects = []
    for time in symbole_time:
        signal = patches.Rectangle((time, 0), 3, 1)
        rects.append(signal)

    pc = PatchCollection(rects, facecolor="yellow", alpha=0.15)

    axes.add_collection(pc)


def _prepare_plot(title, draw_boxes=False, noise_version=0):
    """
    Prepares the plot image with size, labels and title.
    It also adds the noise curve and a dashed line for mark the end of the song.
    """
    fig = plt.figure(figsize=(13, 10))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    _draw_noise_function(noise_version)

    if draw_boxes:
        _draw_signal_boxes(ax)

    plt.xlabel("Zeit [sec]")
    plt.ylabel("Nutzerwertung [a. u.]")
    plt.title(title)

    plt.vlines(68, 0, 1, colors="k", linestyles="dashed")


def create_error_timeline_plot(
    reordered_timeline_df, noise_version=0, draw_signal_boxes=False
):
    """
    Create plots for mean and median. But work is in progress
    """

    _prepare_plot("Median", draw_signal_boxes, noise_version)
    # sns.relplot(x='created_at_relative', y='stdev', kind='line', data=reordered_timeline_df)
    sns.scatterplot(
        x="created_at_relative",
        y="mean",
        data=reordered_timeline_df,
        edgecolor="green",
        color="green",
        alpha=0.4,
    )

    plt.show()
    plt.close("all")


def create_and_save_scatter_plot(
    timeline_df,
    title,
    output_filename,
    draw_noise=0,
    draw_signal_boxes=False,
    dataResampled=False,
    testPlot=False,
):
    """
    Creates and save a scatter plot of given data.
    Because of the available data you can choose between original data plot or resampled plot.
    Also you can add the noise curve oder the yellow signal boxes if necessary
    """
    end_of_song = 68

    if dataResampled:
        path = "data/plots/" + output_filename + "/resampled"
    else:
        path = "data/plots/" + output_filename + "/original"

    if not os.path.exists(path):
        os.makedirs(path)

    # prepare legend labels
    legend_labels = [song_ends]
    if draw_noise != 0:
        legend_labels.append(patch_noise_plot)
    if draw_signal_boxes:
        legend_labels.append(patch_yellow_box)
    if dataResampled:
        legend_labels.append(rating_resampled_dot)
    else:
        legend_labels.append(rating_origin)

    for i, (soSci_survey_Id, data) in enumerate(timeline_df.groupby("soSci_survey_Id")):
        _prepare_plot(title + str(soSci_survey_Id), draw_signal_boxes, draw_noise)

        sns.scatterplot(
            x="created_at_relative",
            y="x",
            data=data,
            edgecolor="green",
            color="green",
            alpha=0.4,
        )

        # marks the end of the song
        plt.vlines(end_of_song, 0, 1, colors="k", linestyles="dashed")

        plt.legend(handles=legend_labels)

        if testPlot:
            plt.show()
            break

        plt.savefig(path + "/" + str(soSci_survey_Id) + ".png")
        # plt.savefig(path+soSci_survey_Id+".svg")

        plt.clf()
        plt.close("all")


def create_and_save_line_and_scatter_plot(
    timeline_origin_df,
    timeline_resampled_df,
    title,
    output_filename,
    draw_noise=0,
    draw_signal_boxes=False,
    testPlot=False,
):
    """
    Creates and save a scatter plot with a line plot of given data.
    Because of the available data it is a nice overview to plot the original data and the resample data as a line plot.
    Therefor you the continuous slider position and see when the users changed it.
    Also you can add the noise curve oder the yellow signal boxes if necessary
    """
    end_of_song = 68

    path = "data/plots/" + output_filename + "/original_resampled"
    if not os.path.exists(path):
        os.makedirs(path)

    # prepare legend labels
    legend_labels = [song_ends]

    if draw_noise != 0:
        legend_labels.append(patch_noise_plot)
    if draw_signal_boxes:
        legend_labels.append(patch_yellow_box)

    legend_labels.append(rating_origin)
    legend_labels.append(rating_resampled_line)

    # regroupe resampled data by soSci_survey_id
    timeline_resampled_group = timeline_resampled_df.groupby("soSci_survey_Id")

    for i, (soSci_survey_Id, data) in enumerate(
        timeline_origin_df.groupby("soSci_survey_Id")
    ):
        _prepare_plot(title + str(soSci_survey_Id), draw_signal_boxes, draw_noise)

        sns.scatterplot(
            x="created_at_relative",
            y="x",
            data=data,
            edgecolor="green",
            color="green",
            alpha=0.4,
        )
        sns.lineplot(
            x="created_at_relative",
            y="x",
            data=timeline_resampled_group.get_group(soSci_survey_Id),
            color="green",
        )

        plt.vlines(end_of_song, 0, 1, colors="k", linestyles="dashed")

        plt.legend(handles=legend_labels)

        if testPlot:
            plt.show()
            break
        else:
            plt.savefig(path + "/" + str(soSci_survey_Id) + ".png")
            # plt.savefig(path+soSci_survey_Id+".svg")

        plt.clf()
        plt.close("all")
