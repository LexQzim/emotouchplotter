"""
Main script to start it all
"""

import os
import sys

import pandaReader as pr
import seabornDrawer as sd

import pandas as pd

import plotSettings as ps


def get_and_plot_timeline_data(
    filename, delimiter, title, draw_signal_boxes, draw_noise, do_extra=False
):
    """
    This method can do everything what you want for one session
    :filename: this is the name of the session
    :delimiter: this is the .csv delimiter. You set this emotouch before you load the data
    :draw_signal_boxes: when True then it will draw yellow boxes
    :draw_noise: You can choose a noise type between 0, 1 and 2
    :doExtra: If True, then this will also find last ticks and calc mean median and standard deviation and reorder the list
    """
    timeline_df = pr.read_and_merge_timeline_data(
        filename + ps.timeline_data_ending,
        filename + ps.session_metadata_ending,
        delimiter,
        ps.needed_ids,
        output_filename=filename,
    )
    sd.create_and_save_scatter_plot(
        timeline_df,
        title,
        output_filename=filename,
        noise=draw_noise,
        draw_signal_boxes=draw_signal_boxes,
    )
    if do_extra:
        reorderd_timeline_data = pr.reorder_timeline_data(timeline_df)
        pr.find_last_ticks_and_save_to_csv(reorderd_timeline_data, filename)
        pr.calc_mean_median_stdev(reorderd_timeline_data, filename)


def get_and_plot_multiple_timeline_data(
    filename_origin,
    filename_resampled,
    delimiter_origin,
    delimiter_resampled,
    title,
    draw_signal_boxes,
    draw_noise,
):
    timeline_origin_df = pr.read_and_merge_timeline_data(
        filename_origin + ps.timeline_data_ending,
        filename_origin + ps.session_metadata_ending,
        delimiter_origin,
        ps.needed_ids,
    )
    timeline_resampled_df = pr.read_and_merge_timeline_data(
        filename_resampled + ps.timeline_data_ending,
        filename_resampled + ps.session_metadata_ending,
        delimiter_resampled,
        ps.needed_ids,
    )

    sd.create_and_save_line_and_scatter_plot(
        timeline_origin_df,
        timeline_resampled_df,
        title,
        output_filename=filename_origin,
        noise=draw_noise,
        draw_signal_boxes=draw_signal_boxes,
    )


def filter_timeline_data_for_blur_and_focus(filename):
    timeline_resampled_df = pr.read_and_merge_timeline_data(
        filename + ps.version_1_7_ending + ps.timeline_data_ending,
        filename + ps.version_1_7_ending + ps.session_metadata_ending,
        delimiter=";",
        needed_ids=ps.needed_ids,
        output_filename=filename,
    )
    timeline_origin_df_blur = pr.read_and_merge_timeline_data(
        filename + ps.timeline_data_ending,
        filename + ps.session_metadata_ending,
        delimiter="\t",
        needed_ids=ps.needed_ids,
        tick_type="BLUR",
    )

    timeline_origin_df_focus = pr.read_and_merge_timeline_data(
        filename + ps.timeline_data_ending,
        filename + ps.session_metadata_ending,
        delimiter="\t",
        needed_ids=ps.needed_ids,
        tick_type="FOCUS",
    )
    reorderd_timeline_data = pr.reorder_timeline_data(timeline_resampled_df)

    pr.get_blur_and_max_min(
        reorderd_timeline_data,
        timeline_origin_df_blur,
        timeline_origin_df_focus,
        filename,
    )


def plot_all_single_hysteresis(noise, resampled_data=False):
    center_is_max = [False, True, True, False]
    outputNames = [
        "hysteris_aus_einschleichend_mit_aufforderung",
        "hysteris_ein_ausschleichend_mit_aufforderung",
        "hysteris_ein_ausschleichend_ohne_aufforderung",
        "hysteris_aus_einschleichend_ohne_aufforderung",
    ]

    for i, fileName in enumerate(ps.fileNames):
        if resampled_data:
            fileName = fileName + ps.version_1_7_ending

        refactored_data_df = pd.read_csv(
            "data/refactored/" + fileName + ".csv",
            delimiter=";",
            encoding="utf-8",
            decimal=",",
        )

        # drop unnecessary columns and set time as index
        refactored_data_df.drop(columns="mean", inplace=True)
        refactored_data_df.drop(columns="median", inplace=True)
        refactored_data_df.drop(columns="stdev", inplace=True)
        refactored_data_df = refactored_data_df.set_index("created_at_relative")
        # drop all rows after the time of 68 (official end of song)
        refactored_data_df = refactored_data_df[refactored_data_df.index < 68]

        # get the three largest series
        # ordered_timeline_series = test_df.count().sort_values().tail(3)
        # test_df = test_df.filter(items=ordered_timeline_series.index)

        for soci_id in refactored_data_df:
            # create new dictionary for selected values
            filtered_noise = {"created_at_relative": [], "noise": [], "rating": []}
            # drop all empty rows
            filtered_origin_series = refactored_data_df[soci_id].dropna()

            for timestamp in filtered_origin_series.index:
                # get the noise value which is timley the nearest neighbour to current timestamp
                df_sorted = (
                    noise[i]
                    .iloc[(noise[i]["t"] - timestamp).abs().argsort()[:1]]["db"]
                    .values[0]
                )

                # add all values to dictionary
                filtered_noise["created_at_relative"].append(timestamp)
                filtered_noise["noise"].append(df_sorted)
                filtered_noise["rating"].append(filtered_origin_series[timestamp])

            # parse dictionary to dataFrame
            df_sort = pd.DataFrame(data=filtered_noise, dtype="float32")

            # plot hysteresis
            sd.create_hysteresis_plot(
                df_sort["rating"],
                df_sort["noise"],
                title=ps.hystersis_title_single[i] + " ID: " + str(soci_id),
                y_label="Bewertungseingaben [a.u.]",
                output_filename=outputNames[i] + "_" + str(soci_id),
                center_is_max=center_is_max[i],
                path="data/plots/hysteresis_single/" + outputNames[i] + "/",
            )


def plot_all_mean_hysteresis(reorderd_timeline_data_cutted, filtered=False):
    if filtered:
        path = "data/plots/hysteresis_filtered/"
    else:
        path = "data/plots/hysteresis/"
    # hysteresis plot
    sd.create_hysteresis_plot(
        reorderd_timeline_data_cutted[1]["mean"],
        noise_1["db"],
        title=ps.hystersis_title_mean[1],
        y_label="Mittelwert der Bewertungseingaben [a.u.]",
        output_filename="hysteris_ein_ausschleichend_mit_aufforderung",
        center_is_max=True,
        path=path,
    )

    sd.create_hysteresis_plot(
        reorderd_timeline_data_cutted[2]["mean"],
        noise_1["db"],
        title=ps.hystersis_title_mean[2],
        y_label="Mittelwert der Bewertungseingaben [a.u.]",
        output_filename="hysteris_ein_ausschleichend_ohne_aufforderung",
        center_is_max=True,
        path=path,
    )

    sd.create_hysteresis_plot_compare(
        reorderd_timeline_data_cutted[1]["mean"],
        reorderd_timeline_data_cutted[2]["mean"],
        noise_1["db"],
        title=ps.hystersis_title_compare[0],
        start_at_zero=True,
        output_filename="vergleich_hysterese_ein_ausschleichend",
        path=path,
    )

    # get first max and drop all values before that
    firstMax = noise_2["db"].iloc[:200].idxmax()
    filtered_noise = noise_2.drop(noise_2.iloc[:firstMax].index)
    # the droped values are the ramped noise values and causing issues
    filtered_mean_values_1 = reorderd_timeline_data_cutted[0].drop(
        reorderd_timeline_data_cutted[0].iloc[:firstMax].index
    )

    sd.create_hysteresis_plot(
        filtered_mean_values_1["mean"],
        filtered_noise["db"],
        title=ps.hystersis_title_mean[0],
        y_label="Mittelwert der Bewertungseingaben [a.u.]",
        output_filename="hysteris_aus_einschleichend_mit_aufforderung",
        center_is_max=False,
        path=path,
    )

    filtered_mean_values_2 = reorderd_timeline_data_cutted[3].drop(
        reorderd_timeline_data_cutted[3].iloc[:firstMax].index
    )

    sd.create_hysteresis_plot(
        filtered_mean_values_2["mean"],
        filtered_noise["db"],
        title=ps.hystersis_title_mean[3],
        y_label="Mittelwert der Bewertungseingaben [a.u.]",
        output_filename="hysteris_aus_einschleichend_ohne_aufforderung",
        center_is_max=False,
        path=path,
    )

    sd.create_hysteresis_plot_compare(
        filtered_mean_values_2["mean"],
        filtered_mean_values_1["mean"],
        filtered_noise["db"],
        title=ps.hystersis_title_compare[1],
        start_at_zero=False,
        output_filename="vergleich_hysterese_aus_einschleichend",
        path=path,
    )


def calc_and_plot_mean_values(filtered=False):
    bad_ids = [447, 453, 487, 487, 490, 552, 584, 611, 664, 688, 700, 701]

    # mean time line plot
    reorderd_timeline_data = []
    reorderd_timeline_data_cutted = []

    path = "data/plots/mean/"

    for i, fileName in enumerate(ps.fileNames):
        # get refactored timeline csv data
        reordered_timeline = pd.read_csv(
            "data/refactored/" + fileName + ps.version_1_7_ending + ".csv",
            delimiter=";",
            encoding="utf-8",
            decimal=",",
            dtype="float",
        )

        if filtered:
            for id in bad_ids:
                if str(id) in reordered_timeline.columns:
                    reordered_timeline.drop(str(id), inplace=True, axis=1)
            path = "data/plots/mean_filtered/"

        # create plot and save it
        sd.create_mean_timeline_plot(
            reordered_timeline,
            output_filename=fileName + ps.version_1_7_ending,
            title=ps.mean_titles[i],
            noise=noise[i],
            draw_signal_boxes=ps.symbol_used[i],
            path=path,
        )

        # drop all values after 68 seconds
        cutted = reordered_timeline.drop(
            reordered_timeline[reordered_timeline["created_at_relative"] > 68].index
        )

        # create plot and save it of cutted data
        sd.create_mean_timeline_plot(
            cutted,
            output_filename=fileName + ps.version_1_7_ending + "_cutted",
            title=ps.mean_titles_cutted[i],
            noise=noise[i],
            draw_signal_boxes=ps.symbol_used[i],
            path=path,
        )

        # add both list to new list for return
        reorderd_timeline_data.append(reordered_timeline)
        reorderd_timeline_data_cutted.append(cutted)

    return [reorderd_timeline_data, reorderd_timeline_data_cutted]


def create_extra_mean_plots(reorderd_timeline_data_cutted, filtered=False):
    if filtered:
        path = "data/plots/mean_filtered/"
    else:
        path = "data/plots/mean/"

    # create comparison plot
    sd.create_and_compare_mean_timeline_plots(
        reorderd_timeline_data_cutted[0],
        reorderd_timeline_data_cutted[3],
        output_filename="vergleich_aus_einschleichend_mittelwerte",
        title=ps.mean_title_compare[1],
        noise=noise_2,
        draw_signal_boxes=False,
        path=path,
    )
    sd.create_and_compare_mean_timeline_plots(
        reorderd_timeline_data_cutted[1],
        reorderd_timeline_data_cutted[2],
        output_filename="vergleich_ein_ausschleichend_mittelwerte",
        title=ps.mean_title_compare[0],
        noise=noise_1,
        draw_signal_boxes=False,
        path=path,
    )

    # calc difference between mean rating and real noise values
    mean_noise_diff = pd.DataFrame(
        {
            "created_at_relative": noise_2["t"],
            "mean": reorderd_timeline_data_cutted[0]["mean"] - noise_2["db"],
        }
    )

    # plot diff
    sd.create_mean_timeline_plot(
        mean_noise_diff,
        output_filename="differenz_rauschen_mittelwerte_aus_einschleichend",
        title=ps.mean_titles_difference[0],
        noise=noise_2,
        draw_signal_boxes=False,
        path=path,
    )

    mean_noise_diff = pd.DataFrame(
        {
            "created_at_relative": noise_1["t"],
            "mean": reorderd_timeline_data_cutted[1]["mean"] - noise_1["db"],
        }
    )

    sd.create_mean_timeline_plot(
        mean_noise_diff,
        output_filename="differenz_rauschen_mittelwerte_ein_ausschleichend",
        title=ps.mean_titles_difference[1],
        noise=noise_1,
        draw_signal_boxes=False,
        path=path,
    )


def test_plots():
    ###### TEST
    timeline_origin_df = pr.read_and_merge_timeline_data(
        "test_timeline_data",
        "test_session_metadata",
        delimiter="\t",
        needed_ids=ps.needed_ids,
        output_filename="filtered_testoutput_origin",
    )
    timeline_resampled_df = pr.read_and_merge_timeline_data(
        "test_resampled_timeline_data",
        "test_resampled_session_metadata",
        delimiter=";",
        needed_ids=ps.needed_ids,
        output_filename="filtered_testoutput_resampled",
    )

    sd.create_and_save_scatter_plot(
        timeline_origin_df,
        title="SoSci Survey Id: ",
        output_filename="test_plot",
        noise=True,
        draw_signal_boxes=True,
        testPlot=False,
    )
    sd.create_and_save_line_and_scatter_plot(
        timeline_origin_df,
        timeline_resampled_df,
        title="SoSci Survey Id: ",
        output_filename="test_plot",
        noise=True,
        draw_signal_boxes=True,
        testPlot=False,
    )
    sd.create_and_save_scatter_plot(
        timeline_resampled_df,
        title="SoSci Survey Id: ",
        output_filename="test_plot",
        noise=noise_1,
        draw_signal_boxes=True,
        testPlot=False,
        dataResampled=True,
    )
    reorderd_timeline_data = pr.reorder_timeline_data(timeline_resampled_df)
    pr.find_last_ticks_and_save_to_csv(reorderd_timeline_data, "test")
    reorderd_timeline_data = pr.calc_mean_median_stdev(reorderd_timeline_data, "test")
    sd.create_mean_timeline_plot(
        reorderd_timeline_data, "test_mean", noise_2, draw_signal_boxes=False
    )

    reorderd_timeline_data = reorderd_timeline_data.reset_index()
    reorderd_timeline_data = reorderd_timeline_data.drop(
        reorderd_timeline_data[reorderd_timeline_data["created_at_relative"] > 68].index
    )
    sd.create_mean_timeline_plot(
        reorderd_timeline_data, "test_mean_cutted", noise_2, draw_signal_boxes=False
    )

    print(len(reorderd_timeline_data))
    print(len(noise_2))

    diff = pd.DataFrame(
        {
            "created_at_relative": noise_2["t"],
            "mean": (noise_2["db"] - reorderd_timeline_data["mean"]),
        }
    )

    print(diff.head())
    sd.create_mean_timeline_plot(diff, "test_diff", noise_2, draw_signal_boxes=False)

    timeline_origin_df_blur = pr.read_and_merge_timeline_data(
        "test_timeline_data",
        "test_session_metadata",
        delimiter="\t",
        needed_ids=ps.needed_ids,
        tick_type="BLUR",
    )

    timeline_origin_df_focus = pr.read_and_merge_timeline_data(
        "test_timeline_data",
        "test_session_metadata",
        delimiter="\t",
        needed_ids=ps.needed_ids,
        tick_type="FOCUS",
    )

    pr.get_blur_and_max_min(
        reorderd_timeline_data,
        timeline_origin_df_blur,
        timeline_origin_df_focus,
        "test",
    )

    pr.read_noise_values("noise_1_8000mhz")
    pr.read_noise_values("noise_2_8000mhz")


if __name__ == "__main__":
    PATH = "data/origin/"
    if not os.path.exists(PATH):
        os.makedirs(PATH)

    if len(os.listdir(PATH)) == 0:
        print("You need to place first your .csv files into this directory.")
        sys.exit()

    noise_1 = pr.read_noise_values("noise_1_8000mhz_linear")
    noise_2 = pr.read_noise_values("noise_2_8000mhz_linear")

    noise = [noise_2, noise_1, noise_1, noise_2]
    filter_means = False

    reordered_timeline_data, reordered_timeline_data_cutted = calc_and_plot_mean_values(
        filtered=filter_means
    )

    create_extra_mean_plots(reordered_timeline_data_cutted, filtered=filter_means)

    plot_all_single_hysteresis(noise)

    plot_all_mean_hysteresis(reordered_timeline_data_cutted, filtered=filter_means)

    for i, fileName in enumerate(ps.fileNames):
        filter_timeline_data_for_blur_and_focus(fileName)
        # you can outcomment the operations with #

        # original data
        get_and_plot_timeline_data(
            filename=fileName,
            delimiter="\t",
            title=ps.titles[i],
            draw_signal_boxes=ps.symbol_used[i],
            draw_noise=noise[i],
            do_extra=True,
        )

        # resampled data (100 ms)
        get_and_plot_timeline_data(
            filename=ps.fileNames[i] + ps.version_1_7_ending,
            title=ps.titles[i],
            delimiter=";",
            draw_signal_boxes=ps.symbol_used[i],
            draw_noise=noise[i],
            do_extra=True,
        )

        #     #  plot both original and resampled data in one image
        get_and_plot_multiple_timeline_data(
            filename_origin=ps.fileNames[i],
            filename_resampled=ps.fileNames[i] + ps.version_1_7_ending,
            delimiter_origin="\t",
            title=ps.titles[i],
            delimiter_resampled=";",
            draw_signal_boxes=ps.symbol_used[i],
            draw_noise=noise[i],
        )
