"""
Main script to start it all
"""

import os
import sys

import pandaReader as pr
import seabornDrawer as sd


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# this is a list for four file sessions.
# Update this list with your names
# Keep in mind that you also need to update the list symbol_used, noise_versions and titles
# all this lists need the same amount of elements
# please pay attention to spacebars. Replace them with underscore (_)
fileNames = [
    "emoTouch_aus_einschleichend_MIT_aufforderung",
    "emoTouch_pretest_ein_ausschleichend_MIT_aufforderung",
    "emoTouch_pretest_ein_ausschleichend_ohne_aufforderung",
    "emoTouch_aus_einschleichend_ohne_neu",
]

# you can update this ending if it doesn't fits your needs
# these are the default endings wich are added to all emotouch .csv-files
timeline_data_ending = "_timeline_data_v1.6.1"
session_metadata_ending = "_session_metadata_v1.6.1"
version_1_7_ending = "_version1.7_(100_ms)"

# This is a list of all soSci Survey Ids which you want to have in your results.
# You need to update this list for your needs
needed_ids = [
    441,
    442,
    447,
    453,
    475,
    477,
    486,
    487,
    490,
    494,
    498,
    503,
    520,
    524,
    530,
    531,
    532,
    534,
    535,
    538,
    539,
    545,
    547,
    550,
    552,
    560,
    565,
    569,
    571,
    574,
    575,
    576,
    584,
    585,
    593,
    595,
    611,
    615,
    616,
    621,
    622,
    635,
    659,
    664,
    667,
    676,
    677,
    681,
    688,
    693,
    700,
    701,
    705,
    721,
    726,
    728,
    746,
    748,
    756,
    761,
    766,
    767,
    770,
    773,
    780,
    781,
    785,
    788,
    798,
    808,
    811,
    812,
    814,
    823,
    839,
    845,
    847,
    859,
    866,
    867,
    868,
    878,
    880,
    883,
    887,
    889,
    890,
    891,
    893,
    906,
    907,
    912,
    913,
    917,
    931,
    937,
    948,
]

# this is a very specific case which you are generaly don't need.
# Just type False for the amount of your used files
symbol_used = [True, True, False, False]

# update for each file type your plot titles
titles = [
    "Versuch:  aus- und einschleichendes Rauschen mit Aufforderung, ID: ",
    "Versuch: ein- und ausschleichendes Rauschen mit Aufforderung, ID: ",
    "Versuch: ein- und ausschleichendes Rauschen ohne Aufforderung, ID: ",
    "Versuch: aus- und einschleichendes Rauschen ohne Aufforderung, ID: ",
]


def call_operations_1(
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
        filename + timeline_data_ending,
        filename + session_metadata_ending,
        delimiter,
        needed_ids,
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


def call_operations_2(
    filename_origin,
    filename_resampled,
    delimiter_origin,
    delimiter_resampled,
    title,
    draw_signal_boxes,
    draw_noise,
):
    timeline_origin_df = pr.read_and_merge_timeline_data(
        filename_origin + timeline_data_ending,
        filename_origin + session_metadata_ending,
        delimiter_origin,
        needed_ids,
    )
    timeline_resampled_df = pr.read_and_merge_timeline_data(
        filename_resampled + timeline_data_ending,
        filename_resampled + session_metadata_ending,
        delimiter_resampled,
        needed_ids,
    )

    sd.create_and_save_line_and_scatter_plot(
        timeline_origin_df,
        timeline_resampled_df,
        title,
        output_filename=filename_origin,
        noise=draw_noise,
        draw_signal_boxes=draw_signal_boxes,
    )


def call_operations_3(filename):
    timeline_resampled_df = pr.read_and_merge_timeline_data(
        filename + version_1_7_ending + timeline_data_ending,
        filename + version_1_7_ending + session_metadata_ending,
        delimiter=";",
        needed_ids=needed_ids,
        output_filename=filename,
    )
    timeline_origin_df_blur = pr.read_and_merge_timeline_data(
        filename + timeline_data_ending,
        filename + session_metadata_ending,
        delimiter="\t",
        needed_ids=needed_ids,
        tick_type="BLUR",
    )

    timeline_origin_df_focus = pr.read_and_merge_timeline_data(
        filename + timeline_data_ending,
        filename + session_metadata_ending,
        delimiter="\t",
        needed_ids=needed_ids,
        tick_type="FOCUS",
    )
    reorderd_timeline_data = pr.reorder_timeline_data(timeline_resampled_df)

    pr.get_blur_and_max_min(
        reorderd_timeline_data,
        timeline_origin_df_blur,
        timeline_origin_df_focus,
        filename,
    )


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
    for i, fileName in enumerate(fileNames):
        call_operations_3(fileName)
        # you can outcomment the operations with #

        # original data
        call_operations_1(
            filename=fileName,
            delimiter="\t",
            title=titles[i],
            draw_signal_boxes=symbol_used[i],
            draw_noise=noise[i],
        )

        # resampled data (100 ms)
        call_operations_1(
            filename=fileNames[i] + version_1_7_ending,
            title=titles[i],
            delimiter=";",
            draw_signal_boxes=symbol_used[i],
            draw_noise=noise[i],
            do_extra=True,
        )

        #  plot both original and resampled data in one image
        call_operations_2(
            filename_origin=fileNames[i],
            filename_resampled=fileNames[i] + version_1_7_ending,
            delimiter_origin="\t",
            title=titles[i],
            delimiter_resampled=";",
            draw_signal_boxes=symbol_used[i],
            draw_noise=noise[i],
        )

    # mean time line plot
    reorderd_timeline_data = []
    reorderd_timeline_data_cutted = []

    for i, fileName in enumerate(fileNames):
        reordered_timeline = pd.read_csv(
            "data/refactored/" + fileName + version_1_7_ending + ".csv",
            delimiter=";",
            encoding="utf-8",
            decimal=",",
            dtype="float",
        )

        sd.create_mean_timeline_plot(
            reordered_timeline,
            fileName,
            noise=noise[i],
            draw_signal_boxes=symbol_used[i],
        )

        reorderd_timeline_data.append(reordered_timeline)
        cutted = reordered_timeline.drop(
            reordered_timeline[reordered_timeline["created_at_relative"] > 68].index
        )
        reorderd_timeline_data_cutted.append(cutted)

        sd.create_mean_timeline_plot(
            cutted,
            fileName + "_cutted",
            noise=noise[i],
            draw_signal_boxes=symbol_used[i],
        )

    sd.create_multiple_mean_timeline_plot(
        reorderd_timeline_data_cutted[0],
        reorderd_timeline_data_cutted[3],
        "kurve_2",
        noise=noise_2,
        draw_signal_boxes=False,
    )
    sd.create_multiple_mean_timeline_plot(
        reorderd_timeline_data_cutted[1],
        reorderd_timeline_data_cutted[2],
        "kurve_1",
        noise=noise_1,
        draw_signal_boxes=False,
    )

    diff = pd.DataFrame(
        {
            "created_at_relative": noise_2["t"],
            "mean": reorderd_timeline_data_cutted[0]["mean"] - noise_2["db"],
        }
    )

    sd.create_mean_timeline_plot(
        diff,
        "diff_2",
        noise=noise_2,
        draw_signal_boxes=False,
    )

    diff = pd.DataFrame(
        {
            "created_at_relative": noise_1["t"],
            "mean": reorderd_timeline_data_cutted[1]["mean"] - noise_1["db"],
        }
    )

    sd.create_mean_timeline_plot(
        diff,
        "diff_1",
        noise=noise_1,
        draw_signal_boxes=False,
    )

    # hysteresis plot
    sd.create_hysteresis_plot(
        reorderd_timeline_data_cutted[1]["mean"],
        noise_1["db"],
        noise_type="Ein-Ausschleichend mit Aufforderung",
        output_filename="hysteris_ein_ausschleichend_mit_aufforderung",
        center_is_max=True,
    )

    sd.create_hysteresis_plot(
        reorderd_timeline_data_cutted[2]["mean"],
        noise_1["db"],
        noise_type="Ein-Ausschleichend ohne Aufforderung",
        output_filename="hysteris_ein_ausschleichend_ohne_aufforderung",
        center_is_max=True,
    )

    sd.create_hysteresis_plot_compare(
        reorderd_timeline_data_cutted[2]["mean"],
        reorderd_timeline_data_cutted[1]["mean"],
        noise_1["db"],
        noise_type="Ein-Ausschleichend",
        output_filename="compare_hysteresis_1",
    )

    firstMax = noise_2["db"].iloc[:200].idxmax()

    tmp_noise = noise_2.drop(noise_2.iloc[:firstMax].index)
    tmp_1 = reorderd_timeline_data_cutted[0].drop(
        reorderd_timeline_data_cutted[0].iloc[:firstMax].index
    )

    sd.create_hysteresis_plot(
        tmp_1["mean"],
        tmp_noise["db"],
        noise_type="Aus-Einschleichend mit Aufforderung",
        output_filename="hysteris_aus_einschleichend_mit_aufforderung",
        center_is_max=False,
    )

    tmp_2 = reorderd_timeline_data_cutted[3].drop(
        reorderd_timeline_data_cutted[3].iloc[:firstMax].index
    )

    sd.create_hysteresis_plot(
        tmp_2["mean"],
        tmp_noise["db"],
        noise_type="Aus-Einschleichend ohne Aufforderung",
        output_filename="hysteris_aus_einschleichend_ohne_aufforderung",
        center_is_max=False,
    )

    sd.create_hysteresis_plot_compare(
        tmp_1["mean"],
        tmp_2["mean"],
        tmp_noise["db"],
        noise_type="Aus-Einschleichend",
        output_filename="compare_hysteresis_2",
    )

    # timeline_origin_df = pr.read_and_merge_timeline_data("test_timeline_data", "test_session_metadata", delimiter="\t", needed_ids=needed_ids, output_filename="filtered_testoutput_origin")
    # timeline_resampled_df = pr.read_and_merge_timeline_data(
    #     "test_resampled_timeline_data",
    #     "test_resampled_session_metadata",
    #     delimiter=";",
    #     needed_ids=needed_ids,
    #     output_filename="filtered_testoutput_resampled",
    # )

    # sd.create_and_save_scatter_plot(timeline_origin_df, title="SoSci Survey Id: ", output_filename="test_plot", draw_noise=1, draw_signal_boxes=True, testPlot=False)
    # sd.create_and_save_line_and_scatter_plot(timeline_origin_df, timeline_resampled_df, title="SoSci Survey Id: ", output_filename="test_plot", draw_noise=1, draw_signal_boxes=True, testPlot=False)
    # sd.create_and_save_scatter_plot(
    #     timeline_resampled_df,
    #     title="SoSci Survey Id: ",
    #     output_filename="test_plot",
    #     noise=noise_1,
    #     draw_signal_boxes=True,
    #     testPlot=False,
    #     dataResampled=True,
    # )
    # reorderd_timeline_data = pr.reorder_timeline_data(timeline_resampled_df)
    # pr.find_last_ticks_and_save_to_csv(reorderd_timeline_data, "test")
    # reorderd_timeline_data = pr.calc_mean_median_stdev(reorderd_timeline_data, "test")
    # sd.create_mean_timeline_plot(
    #     reorderd_timeline_data, "test_mean", noise_2, draw_signal_boxes=False
    # )

    # reorderd_timeline_data = reorderd_timeline_data.reset_index()
    # reorderd_timeline_data = reorderd_timeline_data.drop(
    #     reorderd_timeline_data[reorderd_timeline_data["created_at_relative"] > 68].index
    # )
    # sd.create_mean_timeline_plot(
    #     reorderd_timeline_data, "test_mean_cutted", noise_2, draw_signal_boxes=False
    # )

    # print(len(reorderd_timeline_data))
    # print(len(noise_2))

    # diff = pd.DataFrame(
    #     {
    #         "created_at_relative": noise_2["t"],
    #         "mean": (noise_2["db"] - reorderd_timeline_data["mean"]),
    #     }
    # )

    # print(diff.head())
    # sd.create_mean_timeline_plot(diff, "test_diff", noise_2, draw_signal_boxes=False)

    # sd.create_mean_timeline_plot(reorderd_timeline_data, noise_version=1)

    # timeline_origin_df_blur = pr.read_and_merge_timeline_data(
    #     "test_timeline_data",
    #     "test_session_metadata",
    #     delimiter="\t",
    #     needed_ids=needed_ids,
    #     tick_type="BLUR",
    # )

    # timeline_origin_df_focus = pr.read_and_merge_timeline_data(
    #     "test_timeline_data",
    #     "test_session_metadata",
    #     delimiter="\t",
    #     needed_ids=needed_ids,
    #     tick_type="FOCUS",
    # )

    # pr.get_blur_and_max_min(
    #     reorderd_timeline_data,
    #     timeline_origin_df_blur,
    #     timeline_origin_df_focus,
    #     "test",
    # )

    # pr.read_noise_values("noise_1_8000mhz")
    # pr.read_noise_values("noise_2_8000mhz")
