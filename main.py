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
    "Versuch: aus- und einschleichendes Rauschen mit Aufforderung, ID: ",
    "Versuch: ein- und ausschleichendes Rauschen mit Aufforderung, ID: ",
    "Versuch: ein- und ausschleichendes Rauschen ohne Aufforderung, ID: ",
    "Versuch: aus- und einschleichendes Rauschen ohne Aufforderung, ID: ",
]

hystersis_title_single = [
    "Bewertungseingaben mit Aufforderung, \n aufgetragen gegenüber einer normierten aus-einschleichenden Rauschkurve.",
    "Bewertungseingaben mit Aufforderung, \n aufgetragen gegenüber einer normierten ein-ausschleichenden Rauschkurve.",
    "Bewertungseingaben ohne Aufforderung, \n aufgetragen gengegenüber einer normierten ein-ausschleichenden Rauschkurve.",
    "Bewertungseingaben ohne Aufforderung, \n aufgetragen gegenüber einer normierten aus-einschleichenden Rauschkurve.",
]

hystersis_title_mean = [
    "Gemittelte Bewertungseingaben mit Aufforderung, \n aufgetragen gegenüber einer normierten aus-einschleichenden Rauschkurve.",
    "Gemittelte Bewertungseingaben mit Aufforderung, \n aufgetragen gegenüber einer normierten ein-ausschleichenden Rauschkurve.",
    "Gemittelte Bewertungseingaben ohne Aufforderung, \n aufgetragen gegenüber einer normierten ein-ausschleichenden Rauschkurve.",
    "Gemittelte Bewertungseingaben ohne Aufforderung, \n aufgetragen gegenüber einer normierten aus-einschleichenden Rauschkurve.",
]

hystersis_title_compare = [
    "Vergleich zweier gemittelter Bewertungseingaben, \n aufgetragen gegenüber einer ein-ausschleichenden Rauschkurve",
    "Vergleich zweier gemittelter Bewertungseingaben, \n aufgetragen gegenüber einer aus-einschleichenden Rauschkurve",
]

mean_titles = [
    "Gemittelte Bewertungseingaben der aus-einschleichenden Rauschkurve mit Aufforderung",
    "Gemittelte Bewertungseingaben der ein-ausschleichenden Rauschkurve mit Aufforderung",
    "Gemittelte Bewertungseingaben der ein-ausschleichenden Rauschkurve ohne Aufforderung",
    "Gemittelte Bewertungseingaben der aus-einschleichenden Rauschkurve ohne Aufforderung",
]

mean_titles_cutted = [
    "Gemittelte und auf 68 Sekunden beschränkte \nBewertungseingaben der aus-einschleichenden Rauschkurve mit Aufforderung",
    "Gemittelte und auf 68 Sekunden beschränkte \nBewertungseingaben der ein-ausschleichenden Rauschkurve mit Aufforderung",
    "Gemittelte und auf 68 Sekunden beschränkte \nBewertungseingaben der ein-ausschleichenden Rauschkurve ohne Aufforderung",
    "Gemittelte und auf 68 Sekunden beschränkte \nBewertungseingaben der aus-einschleichenden Rauschkurve ohne Aufforderung",
]

mean_titles_diff = [
    "Differenz zwischen den gemittelte Bewertungseingaben \nund der aus-einschleichenden Rauschkurve mit Aufforderung",
    "Differenz zwischen den gmittelte Bewertungseingaben \nund der ein-ausschleichenden Rauschkurve mit Aufforderung",
    "Differenz zwischen den gemittelte Bewertungseingaben \nund der ein-ausschleichenden Rauschkurve ohne Aufforderung",
    "Differenz zwischen den gemittelte Bewertungseingaben \nund der aus-einschleichenden Rauschkurve ohne Aufforderung",
]

mean_title_compare = [
    "Vergleich zweier gemittelter Bewertungseingaben der ein-ausschleichenden Rauschkurve",
    "Vergleich zweier gemittelter Bewertungseingaben der aus-einschleichenden Rauschkurve",
]


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


def filter_timeline_data_for_blur_and_focus(filename):
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


def plot_all_single_hysteresis(noise, resampled_data=False):
    center_is_max = [False, True, True, False]
    outputNames = [
        "hysteris_aus_einschleichend_mit_aufforderung",
        "hysteris_ein_ausschleichend_mit_aufforderung",
        "hysteris_ein_ausschleichend_ohne_aufforderung",
        "hysteris_aus_einschleichend_ohne_aufforderung",
    ]

    for i, fileName in enumerate(fileNames):
        if resampled_data:
            fileName = fileName + version_1_7_ending

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
                title=hystersis_title_single[i] + " ID: " + str(soci_id),
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
        title=hystersis_title_mean[1],
        y_label="Mittelwert der Bewertungseingaben [a.u.]",
        output_filename="hysteris_ein_ausschleichend_mit_aufforderung",
        center_is_max=True,
        path=path,
    )

    sd.create_hysteresis_plot(
        reorderd_timeline_data_cutted[2]["mean"],
        noise_1["db"],
        title=hystersis_title_mean[2],
        y_label="Mittelwert der Bewertungseingaben [a.u.]",
        output_filename="hysteris_ein_ausschleichend_ohne_aufforderung",
        center_is_max=True,
        path=path,
    )

    sd.create_hysteresis_plot_compare(
        reorderd_timeline_data_cutted[1]["mean"],
        reorderd_timeline_data_cutted[2]["mean"],
        noise_1["db"],
        title=hystersis_title_compare[0],
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
        title=hystersis_title_mean[0],
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
        title=hystersis_title_mean[3],
        y_label="Mittelwert der Bewertungseingaben [a.u.]",
        output_filename="hysteris_aus_einschleichend_ohne_aufforderung",
        center_is_max=False,
        path=path,
    )

    sd.create_hysteresis_plot_compare(
        filtered_mean_values_2["mean"],
        filtered_mean_values_1["mean"],
        filtered_noise["db"],
        title=hystersis_title_compare[1],
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

    for i, fileName in enumerate(fileNames):
        # get refactored timeline csv data
        reordered_timeline = pd.read_csv(
            "data/refactored/" + fileName + version_1_7_ending + ".csv",
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
            output_filename=fileName + version_1_7_ending,
            title=mean_titles[i],
            noise=noise[i],
            draw_signal_boxes=symbol_used[i],
            path=path,
        )

        # drop all values after 68 seconds
        cutted = reordered_timeline.drop(
            reordered_timeline[reordered_timeline["created_at_relative"] > 68].index
        )

        # create plot and save it of cutted data
        sd.create_mean_timeline_plot(
            cutted,
            output_filename=fileName + version_1_7_ending + "_cutted",
            title=mean_titles_cutted[i],
            noise=noise[i],
            draw_signal_boxes=symbol_used[i],
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
        title=mean_title_compare[1],
        noise=noise_2,
        draw_signal_boxes=False,
        path=path,
    )
    sd.create_and_compare_mean_timeline_plots(
        reorderd_timeline_data_cutted[1],
        reorderd_timeline_data_cutted[2],
        output_filename="vergleich_ein_ausschleichend_mittelwerte",
        title=mean_title_compare[0],
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
        title=mean_titles_diff[0],
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
        title=mean_titles_diff[1],
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
        needed_ids=needed_ids,
        output_filename="filtered_testoutput_origin",
    )
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

    # for i, fileName in enumerate(fileNames):
    #     filter_timeline_data_for_blur_and_focus(fileName)
    #     # you can outcomment the operations with #

    #     # original data
    #     get_and_plot_timeline_data(
    #         filename=fileName,
    #         delimiter="\t",
    #         title=titles[i],
    #         draw_signal_boxes=symbol_used[i],
    #         draw_noise=noise[i],
    #         do_extra=True,
    #     )

    #     # resampled data (100 ms)
    #     get_and_plot_timeline_data(
    #         filename=fileNames[i] + version_1_7_ending,
    #         title=titles[i],
    #         delimiter=";",
    #         draw_signal_boxes=symbol_used[i],
    #         draw_noise=noise[i],
    #         do_extra=True,
    #     )

    #     #     #  plot both original and resampled data in one image
    #     get_and_plot_multiple_timeline_data(
    #         filename_origin=fileNames[i],
    #         filename_resampled=fileNames[i] + version_1_7_ending,
    #         delimiter_origin="\t",
    #         title=titles[i],
    #         delimiter_resampled=";",
    #         draw_signal_boxes=symbol_used[i],
    #         draw_noise=noise[i],
    #     )
