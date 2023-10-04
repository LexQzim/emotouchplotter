import os

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D
from matplotlib.collections import PatchCollection
import numpy as np
import seaborn as sns

symbole_time = [6, 12, 21, 33, 42, 51, 57, 63]

END_OF_SONG = 68
COLOR_GREEN = "#04a729"
COLOR_YELLOW = "#fad419"

# ALPHA_30 = "55"
# ALPHA_40 = "66"
ALPHA_50 = "7F"
# ALPHA_75 = "AA"

sns.set_theme(style="whitegrid")

# prepare legend
patch_yellow_box = patches.Patch(
    color=COLOR_YELLOW + ALPHA_50,
    label="Aufforderung",
)
patch_noise_plot = patches.Patch(color="#C0C0C055", label="Rauschkurve")
song_ends = Line2D(
    [0], [0], color="k", linestyle="dashed", label="Ende vom Liedausschnitt"
)
rating_origin = Line2D(
    [0],
    [0],
    marker="o",
    markersize=7,
    markerfacecolor=COLOR_GREEN + ALPHA_50,
    linestyle="",
    label="Wertungen (original)",
)
rating_resampled_line = Line2D(
    [0], [0], color=COLOR_GREEN, linestyle="solid", label="Wertungen (resampled)"
)
rating_resampled_dot = Line2D(
    [0],
    [0],
    marker="o",
    markersize=7,
    markerfacecolor=COLOR_GREEN + ALPHA_50,
    linestyle="",
    label="Wertungen (resampled)",
)
mean_rating = Line2D(
    [0],
    [0],
    marker="o",
    markersize=7,
    markerfacecolor=COLOR_GREEN + ALPHA_50,
    linestyle="",
    label="Mittelwert",
)
mean_rating_without = Line2D(
    [0],
    [0],
    marker="o",
    markersize=7,
    markerfacecolor=COLOR_GREEN + ALPHA_50,
    linestyle="",
    label="Mittelwert (ohne Aufforderung)",
)
mean_rating_with = Line2D(
    [0],
    [0],
    marker="o",
    markersize=7,
    markerfacecolor=COLOR_YELLOW + ALPHA_50,
    linestyle="",
    label="Mittelwert (mit Aufforderung)",
)


def _draw_noise(noise):
    plt.fill_between(
        noise.t,
        noise.db,
        alpha=0.5,
        color="silver",
    )


def _draw_signal_boxes(axes):
    """
    Add on given timing vertical yellow boxes to symbolize when the signal is shown
    """
    rects = []
    for time in symbole_time:
        signal = patches.Rectangle((time, 0), 3, 1)
        rects.append(signal)

    pc = PatchCollection(rects, facecolor=COLOR_YELLOW, alpha=0.15)

    axes.add_collection(pc)


def _prepare_plot(title, draw_boxes=False, noise=False):
    """
    Prepares the plot image with size, labels and title.
    It also adds the noise curve and a dashed line for mark the end of the song.
    """
    fig = plt.figure(figsize=(13, 10))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

    if draw_boxes:
        _draw_signal_boxes(ax)
    if noise is not False:
        _draw_noise(noise)

    plt.xlabel("Zeit [sec]", weight="bold")
    plt.ylabel("normiertes Rauschen [a.u.]\n Bewertungen [a.u.]", weight="bold")
    plt.title(title, weight="bold")

    plt.vlines(END_OF_SONG, 0, 1, colors="k", linestyles="dashed")


def create_mean_timeline_plot(
    reordered_timeline_df,
    output_filename="",
    noise=False,
    title="Mittelwert",
    draw_signal_boxes=False,
    path="data/plots/mean/",
):
    """
    Create plots for mean and median. But work is in progress
    """

    if not os.path.exists(path):
        os.makedirs(path)

    # prepare legend labels
    legend_labels = [song_ends]
    if noise is not False:
        legend_labels.append(patch_noise_plot)
    if draw_signal_boxes:
        legend_labels.append(patch_yellow_box)

    legend_labels.append(mean_rating)

    _prepare_plot(title, draw_signal_boxes, noise)

    sns.scatterplot(
        x="created_at_relative",
        y="mean",
        data=reordered_timeline_df,
        edgecolor=COLOR_GREEN,
        color=COLOR_GREEN,
        alpha=0.4,
    )

    plt.legend(handles=legend_labels)

    plt.savefig(path + output_filename + ".png")
    plt.savefig(path + output_filename + ".svg")
    # plt.show()
    plt.close("all")


def create_and_compare_mean_timeline_plots(
    timeline_df_with,
    timeline_df_without,
    output_filename="",
    noise=False,
    title="Mittelwert Vergleich",
    draw_signal_boxes=False,
    path="data/plots/mean/",
):
    """
    Create plots for mean and median. But work is in progress
    """

    if not os.path.exists(path):
        os.makedirs(path)

    # prepare legend labels
    legend_labels = [song_ends]
    if noise is not False:
        legend_labels.append(patch_noise_plot)
    if draw_signal_boxes:
        legend_labels.append(patch_yellow_box)

    legend_labels.append(mean_rating_with)
    legend_labels.append(mean_rating_without)

    _prepare_plot(title, draw_signal_boxes, noise)

    sns.scatterplot(
        x="created_at_relative",
        y="mean",
        data=timeline_df_with,
        edgecolor=COLOR_YELLOW,
        color=COLOR_YELLOW,
        alpha=0.5,
    )
    sns.scatterplot(
        x="created_at_relative",
        y="mean",
        data=timeline_df_without,
        edgecolor=COLOR_GREEN,
        color=COLOR_GREEN,
        alpha=0.5,
    )

    plt.legend(handles=legend_labels)

    plt.savefig(path + output_filename + ".png")
    plt.savefig(path + output_filename + ".svg")
    # plt.show()
    plt.close("all")


def prepare_hysteresis_plot(y_label, title):
    fig = plt.figure(figsize=(13, 10))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

    plt.xlim((0, 1))
    plt.ylim((0, 1))
    plt.xlabel("Normiertes Rauschen [a.u.]", weight="bold")
    plt.ylabel(y_label, weight="bold")
    plt.xticks(np.arange(0, 1.1, step=0.1))
    plt.setp(ax.get_xticklabels()[1::2], visible=False)
    plt.yticks(np.arange(0, 1.1, step=0.1))
    plt.setp(ax.get_yticklabels()[1::2], visible=False)
    plt.title(title, weight="bold")


def create_hysteresis_plot(
    mean_values,
    noise_values,
    title,
    y_label,
    output_filename="",
    center_is_max=True,
    path="data/plots/hysteresis/",
):
    if len(noise_values) < 1:
        print("noise list is to small!")
        return

    # find max or min noise value
    if center_is_max:
        index_of_first_extrema = noise_values.idxmax()
    else:
        index_of_first_extrema = noise_values[noise_values == 0].last_valid_index()
        if index_of_first_extrema == None:
            index_of_first_extrema = noise_values.idxmin()

    # get all maxima/minima and then select the central index.
    # This is the central turning point of noise changes
    central_extrema = noise_values.loc[
        noise_values == noise_values[index_of_first_extrema]
    ].index
    # print(len(central_extrema))
    if len(central_extrema) == 1:
        index_of_center = central_extrema[0]
    else:
        index_of_center = central_extrema[: int(len(central_extrema) / 2)][0]

    # if center_is_max:
    direction = ["up"] * index_of_center
    direction = direction + ["down"] * (len(noise_values) - index_of_center)
    color_palette = [COLOR_GREEN, COLOR_YELLOW]
    # else:
    #     direction = ["down"] * index_of_center
    #     direction = direction + ["up"] * (len(noise_values) - index_of_center)
    #     color_palette = [COLOR_GREEN, COLOR_YELLOW]

    hysterese = pd.DataFrame(
        {
            "noise": noise_values,
            "rating": mean_values,
            "direction": direction,
        }
    )

    prepare_hysteresis_plot(y_label, title)

    sns.scatterplot(
        x="noise",
        y="rating",
        data=hysterese,
        # kind="line",
        marker=".",
        hue="direction",
        legend=False,
        palette=color_palette,
        edgecolor=None,
    )

    legend_dir_1 = Line2D(
        [0],
        [0],
        marker="o",
        markersize=5,
        markerfacecolor=COLOR_GREEN,
        markeredgecolor=COLOR_GREEN,
        linestyle="",
        label="Hinweg",
    )
    legend_dir_2 = Line2D(
        [0],
        [0],
        marker="o",
        markersize=5,
        markerfacecolor=COLOR_YELLOW,
        markeredgecolor=COLOR_YELLOW,
        linestyle="",
        label="Rückweg",
    )

    start = Line2D(
        [0],
        [0],
        marker="o",
        markersize=10,
        color="red",
        linestyle="",
        label="Versuchsanfang",
    )

    plt.legend(handles=[legend_dir_1, legend_dir_2, start])
    if center_is_max:
        start_x = [0]
        start_y = [0.5]
    else:
        start_x = [1]
        start_y = [0.5]

    plt.plot(start_x, start_y, marker="o", markersize=10, color="red")

    # plt.show()

    if output_filename != "":
        if not os.path.exists(path):
            os.makedirs(path)

        plt.savefig(path + output_filename + ".png")
        plt.savefig(path + output_filename + ".svg")

    plt.clf()
    plt.close("all")


def create_hysteresis_plot_compare(
    mean_values_without,
    mean_values_with,
    noise_values,
    title,
    start_at_zero,
    output_filename="",
    path="data/plots/hysteresis/",
):
    noise = pd.concat([noise_values, noise_values])

    mean_val = pd.concat([mean_values_without, mean_values_with])

    direction = ["typ1"] * len(mean_values_without)
    direction = direction + ["typ2"] * len(mean_values_with)

    hysterese = pd.DataFrame(
        {
            "noise": noise,
            "rating": mean_val,
            "direction": direction,
        }
    )

    prepare_hysteresis_plot("Mittelwerte der Bewertungen [u.a.]", title)

    sns.scatterplot(
        x="noise",
        y="rating",
        data=hysterese,
        # kind="line",
        marker=".",
        hue="direction",
        legend=False,
        palette=[COLOR_GREEN, COLOR_YELLOW],
        edgecolor=None,
    )

    legend_dir_1 = Line2D(
        [0],
        [0],
        marker="o",
        markersize=5,
        markerfacecolor=COLOR_GREEN,
        markeredgecolor=COLOR_GREEN,
        linestyle="",
        label="Ohne Aufforderung",
    )
    legend_dir_2 = Line2D(
        [0],
        [0],
        marker="o",
        markersize=5,
        markerfacecolor=COLOR_YELLOW,
        markeredgecolor=COLOR_YELLOW,
        linestyle="",
        label="Mit Aufforderung",
    )

    start = Line2D(
        [0],
        [0],
        marker="o",
        markersize=10,
        color="red",
        linestyle="",
        label="Versuchsanfang",
    )

    plt.legend(handles=[legend_dir_1, legend_dir_2, start])
    if start_at_zero:
        start_x = [0]
        start_y = [0.5]
    else:
        start_x = [1]
        start_y = [0.5]

    plt.plot(start_x, start_y, marker="o", markersize=10, color="red")

    # plt.show()

    if output_filename != "":
        if not os.path.exists(path):
            os.makedirs(path)

        plt.savefig(path + output_filename + ".png")
        plt.savefig(path + output_filename + ".svg")

    plt.clf()
    plt.close("all")


def create_and_save_scatter_plot(
    timeline_df,
    title,
    output_filename,
    noise=False,
    draw_signal_boxes=False,
    dataResampled=False,
    testPlot=False,
):
    """
    Creates and save a scatter plot of given data.
    Because of the available data you can choose between original data plot or resampled plot.
    Also you can add the noise curve oder the yellow signal boxes if necessary
    """

    if dataResampled:
        path = "data/plots/" + output_filename + "/resampled"
    else:
        path = "data/plots/" + output_filename + "/original"

    if not os.path.exists(path):
        os.makedirs(path)

    # prepare legend labels
    legend_labels = [song_ends]
    if noise is not False:
        legend_labels.append(patch_noise_plot)
    if draw_signal_boxes:
        legend_labels.append(patch_yellow_box)
    if dataResampled:
        legend_labels.append(rating_resampled_dot)
    else:
        legend_labels.append(rating_origin)

    for i, (soSci_survey_Id, data) in enumerate(timeline_df.groupby("soSci_survey_Id")):
        _prepare_plot(title + str(soSci_survey_Id), draw_signal_boxes, noise)

        sns.scatterplot(
            x="created_at_relative",
            y="x",
            data=data,
            edgecolor=COLOR_GREEN,
            color=COLOR_GREEN,
            alpha=0.4,
        )

        plt.legend(handles=legend_labels)

        if testPlot:
            plt.show()
            break

        plt.savefig(path + "/" + str(soSci_survey_Id) + ".png")
        plt.savefig(path + "/" + str(soSci_survey_Id) + ".svg")

        plt.clf()
        plt.close("all")


def create_and_save_line_and_scatter_plot(
    timeline_origin_df,
    timeline_resampled_df,
    title,
    output_filename,
    noise=False,
    draw_signal_boxes=False,
    testPlot=False,
):
    """
    Creates and save a scatter plot with a line plot of given data.
    Because of the available data it is a nice overview to plot the original data and the resample data as a line plot.
    Therefor you the continuous slider position and see when the users changed it.
    Also you can add the noise curve oder the yellow signal boxes if necessary
    """

    path = "data/plots/" + output_filename + "/original_resampled"
    if not os.path.exists(path):
        os.makedirs(path)

    # prepare legend labels
    legend_labels = [song_ends]

    if noise is not False:
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
        _prepare_plot(title + str(soSci_survey_Id), draw_signal_boxes, noise)

        sns.scatterplot(
            x="created_at_relative",
            y="x",
            data=data,
            edgecolor=COLOR_GREEN,
            color=COLOR_GREEN,
            alpha=0.4,
        )
        sns.lineplot(
            x="created_at_relative",
            y="x",
            data=timeline_resampled_group.get_group(soSci_survey_Id),
            color=COLOR_GREEN,
        )

        plt.legend(handles=legend_labels)

        if testPlot:
            plt.show()
            break
        else:
            plt.savefig(path + "/" + str(soSci_survey_Id) + ".png")
            plt.savefig(path + "/" + str(soSci_survey_Id) + ".svg")

        plt.clf()
        plt.close("all")
