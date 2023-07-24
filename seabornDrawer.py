import os

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D
from matplotlib.collections import PatchCollection

import seaborn as sns

symbole_time = [6, 12, 21, 33, 42, 51, 57, 63]

END_OF_SONG = 68

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
mean_rating = Line2D(
    [0],
    [0],
    marker="o",
    markersize=10,
    markerfacecolor="#00800055",
    linestyle="",
    label="Mittelwert",
)
mean_rating_without = Line2D(
    [0],
    [0],
    marker="o",
    markersize=10,
    markerfacecolor="#00800055",
    linestyle="",
    label="Mittelwert (ohne Aufforderung)",
)
mean_rating_with = Line2D(
    [0],
    [0],
    marker="o",
    markersize=10,
    markerfacecolor="#FFFF0055",
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

    pc = PatchCollection(rects, facecolor="yellow", alpha=0.15)

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

    plt.xlabel("Zeit in s")
    plt.ylabel("Normierte Skala")
    plt.title(title)

    plt.vlines(68, 0, 1, colors="k", linestyles="dashed")


def create_mean_timeline_plot(
    reordered_timeline_df, output_filename="", noise=False, draw_signal_boxes=False
):
    """
    Create plots for mean and median. But work is in progress
    """
    path = "data/plots/mean/"

    if not os.path.exists(path):
        os.makedirs(path)

    # prepare legend labels
    legend_labels = [song_ends]
    if noise is not False:
        legend_labels.append(patch_noise_plot)
    if draw_signal_boxes:
        legend_labels.append(patch_yellow_box)

    legend_labels.append(mean_rating)

    _prepare_plot("Mittelwert", draw_signal_boxes, noise)

    sns.scatterplot(
        x="created_at_relative",
        y="mean",
        data=reordered_timeline_df,
        edgecolor="green",
        color="green",
        alpha=0.4,
    )

    # marks the end of the song
    plt.vlines(END_OF_SONG, 0, 1, colors="k", linestyles="dashed")

    plt.legend(handles=legend_labels)

    plt.savefig(path + output_filename + ".png")
    plt.savefig(path + output_filename + ".svg")
    # plt.show()
    plt.close("all")


def create_multiple_mean_timeline_plot(
    timeline_df_with,
    timeline_df_without,
    output_filename="",
    noise=False,
    draw_signal_boxes=False,
):
    """
    Create plots for mean and median. But work is in progress
    """
    path = "data/plots/mean/"

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

    _prepare_plot("Mittelwert Vergleich", draw_signal_boxes, noise)

    sns.scatterplot(
        x="created_at_relative",
        y="mean",
        data=timeline_df_with,
        edgecolor="green",
        color="green",
        alpha=0.4,
    )
    sns.scatterplot(
        x="created_at_relative",
        y="mean",
        data=timeline_df_without,
        edgecolor="yellow",
        color="yellow",
        alpha=0.4,
    )
    # marks the end of the song
    plt.vlines(END_OF_SONG, 0, 1, colors="k", linestyles="dashed")

    plt.legend(handles=legend_labels)

    plt.savefig(path + output_filename + ".png")
    plt.savefig(path + output_filename + ".svg")
    # plt.show()
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
            edgecolor="green",
            color="green",
            alpha=0.4,
        )

        # marks the end of the song
        plt.vlines(END_OF_SONG, 0, 1, colors="k", linestyles="dashed")

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

        plt.vlines(END_OF_SONG, 0, 1, colors="k", linestyles="dashed")

        plt.legend(handles=legend_labels)

        if testPlot:
            plt.show()
            break
        else:
            plt.savefig(path + "/" + str(soSci_survey_Id) + ".png")
            plt.savefig(path + "/" + str(soSci_survey_Id) + ".svg")

        plt.clf()
        plt.close("all")
