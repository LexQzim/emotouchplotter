import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

pd.options.display.max_rows = 9999


def read_and_merge_timeline_data(
    timeline_filename,
    session_data_filename,
    delimiter,
    needed_ids,
    output_filename="",
    tick_type="TICKCHANGE",
):
    timeline_df = pd.read_csv(
        "data/origin/" + timeline_filename + ".csv",
        delimiter=delimiter,
        encoding="utf-8",
    )
    session_df = pd.read_csv(
        "data/origin/" + session_data_filename + ".csv",
        delimiter=delimiter,
        encoding="utf-8",
    )

    # merge timeline data and session meta data to get soCiSurvey id
    new_timeline_df = pd.merge(
        timeline_df[["session_id", "x", "created_at_relative", "type"]],
        session_df[["id", "s1"]],
        left_on="session_id",
        right_on="id",
    )
    # reformat time from millisecond to second
    new_timeline_df["created_at_relative"] = (
        new_timeline_df["created_at_relative"] / 1000
    )
    # drop rows with negative created at timestamp
    new_timeline_df = new_timeline_df.drop(
        new_timeline_df[new_timeline_df["created_at_relative"] < 0].index
    )
    # select only rows of type TICKCHANGE
    new_timeline_df = new_timeline_df.drop(
        new_timeline_df[new_timeline_df["type"] != tick_type].index
    )
    # drop dupcliated column
    new_timeline_df = new_timeline_df.drop(columns="id")
    # rename col s1 to soSci_survey_Id
    new_timeline_df = new_timeline_df.rename(columns={"s1": "soSci_survey_Id"})
    # select only specific soci survey ids
    new_timeline_df = new_timeline_df.drop(
        new_timeline_df[~new_timeline_df["soSci_survey_Id"].isin(needed_ids)].index
    )

    if tick_type != "TICKCHANGE":
        new_timeline_df = new_timeline_df.drop(columns="x")
        new_timeline_df = new_timeline_df.astype(
            {
                "session_id": "int16",
                "created_at_relative": "float32",
                "type": "str",
                "soSci_survey_Id": "int16",
            }
        )
    else:
        # drop rows with nan values
        new_timeline_df = new_timeline_df.dropna()
        # set type of each column for savety reasons
        new_timeline_df = new_timeline_df.astype(
            {
                "session_id": "int16",
                "x": "float32",
                "created_at_relative": "float32",
                "type": "str",
                "soSci_survey_Id": "int16",
            }
        )

    # uncomment to get a tablepreview
    # print(new_timeline_df.head())

    # check if path exists. if not then create a new one
    path = "data/clean_and_merged/"
    if not os.path.exists(path):
        os.makedirs(path)

    # create csv of filtered data
    if output_filename != "":
        new_timeline_df.to_csv(
            path + output_filename + ".csv", index=False, decimal=",", sep=";"
        )

    return new_timeline_df


def reorder_timeline_data(timeline_df: pd.DataFrame):
    """
    Reorders the timeline data from default view:
    old header: session_id (old index), x, created_at_relative, type, soci_survey_Id
    to
    new header:
        created_at_relative (new index), 123, 243, 5423, 23, ....

    You can change the header by selecting a differen column in the attribute columns
    """
    timeline_df = timeline_df.pivot_table(
        index=["created_at_relative"], columns=["soSci_survey_Id"], values=["x"]
    )
    timeline_df = timeline_df.droplevel(axis=1, level=0)
    timeline_df = timeline_df.reset_index()
    timeline_df = timeline_df.rename(columns={"soSci_survey_Id": "index"})

    timeline_df = timeline_df.set_index("created_at_relative")

    return timeline_df


def calc_mean_median_stdev(timeline_df: pd.DataFrame, output_filename=""):
    timeline_df["mean"] = timeline_df.mean(axis=1)
    timeline_df["median"] = timeline_df.median(axis=1)
    timeline_df["stdev"] = timeline_df.std(axis=1)

    # reorder header level and give it a propper name
    header = timeline_df.columns.to_list()
    header[-1] = "stdev"
    header[-2] = "median"
    header[-3] = "mean"
    timeline_df.columns = header

    # save file
    path = "data/refactored/"
    if not os.path.exists(path):
        os.makedirs(path)

    if output_filename != "":
        timeline_df.to_csv(path + output_filename + ".csv", decimal=",", sep=";")
    return timeline_df


def find_last_ticks_and_save_to_csv(
    timeline_df: pd.DataFrame, output_filename="", decimal=",", sep=";"
):
    # get all last valid ticks
    last_valid_ticks = timeline_df.apply(pd.Series.last_valid_index)
    # change type
    last_valid_ticks = pd.Series.to_frame(last_valid_ticks)
    # rename column and reset index for clear naming
    last_valid_ticks = last_valid_ticks.reset_index()
    last_valid_ticks.rename(columns={0: "timestamp"}, inplace=True)
    # last_valid_ticks = last_valid_ticks.drop(columns="level_0")

    # check if path exists. if not then create a new one
    path = "data/lastTicks/"
    if not os.path.exists(path):
        os.makedirs(path)

    # create csv of filtered data
    if output_filename != "":
        last_valid_ticks.to_csv(
            path + output_filename + ".csv", index=False, decimal=decimal, sep=sep
        )

    # comment this out to get a preview of found data
    # sns.scatterplot(y='soSci_survey_Id',x='timestamp', data=last_valid_ticks, edgecolor = "green", color = "green", alpha = 0.4)
    # plt.show()


def get_blur_and_max_min(
    timeline_df: pd.DataFrame,
    timeline_blured: pd.DataFrame,
    timeline_focused: pd.DataFrame,
    output_filename="",
):
    print(len(timeline_blured))

    count_of_blur = (
        timeline_blured.groupby(["soSci_survey_Id"]).count()["session_id"].max()
    )

    count_of_focus = (
        timeline_focused.groupby(["soSci_survey_Id"]).count()["session_id"].max()
    )

    fill_blur = [""] * count_of_blur

    fill_focus = [""] * count_of_focus

    column_names = ["soSci_survey_Id", "max", "min"]

    for i in range(count_of_blur):
        column_names += ["blur_" + str(i + 1)]

    for i in range(count_of_focus):
        column_names += ["focus_" + str(i + 1)]

    new_df = pd.DataFrame(columns=column_names)

    for column in timeline_df:
        if column == "created_at_relative":
            continue

        tmp_blur = timeline_blured[timeline_blured["soSci_survey_Id"] == column]

        blur_val = [""]
        if not tmp_blur["created_at_relative"].empty:
            blur_val = (
                tmp_blur["created_at_relative"].to_string(index=False).split("\n")
            )

        blur_val = blur_val[:count_of_blur] + fill_blur[len(blur_val) :]

        tmp_focus = timeline_focused[timeline_focused["soSci_survey_Id"] == column]

        focus_val = [""]
        if not tmp_focus["created_at_relative"].empty:
            focus_val = (
                tmp_focus["created_at_relative"].to_string(index=False).split("\n")
            )

        focus_val = focus_val[:count_of_focus] + fill_focus[len(focus_val) :]

        new_df.loc[-1] = (
            [
                column,
                timeline_df[column].max(),
                timeline_df[column].min(),
            ]
            + blur_val
            + focus_val
        )  # adding a row

        new_df.index = new_df.index + 1  # shifting index
        # new_df = new_df.sort_index()

    new_df = new_df.astype(
        {
            "soSci_survey_Id": "int16",
            "max": "float32",
            "min": "float32",
        }
    )

    # check if path exists. if not then create a new one
    PATH = "data/min_max/"
    if not os.path.exists(PATH):
        os.makedirs(PATH)

    # create csv of filtered data
    if output_filename != "":
        new_df.to_csv(
            PATH + output_filename + ".csv", index=False, decimal=",", sep=";"
        )


def read_noise_values(filename, rescale=True, createPlot=False):
    PATH = "data/noise/"
    df = pd.read_csv(PATH + filename + ".txt", sep="\t", low_memory=False)
    if rescale:
        df = df.drop(df[df["db"] == "[-inf]"].index)
        df = df.drop(df[df["db"] == "[inf]"].index)

    df = df.astype(
        {
            "t": "float32",
            "db": "float32",
        }
    )

    # Min-Max Normalization
    df = df.abs()

    df.to_csv(PATH + filename + ".csv", index=False, decimal=",", sep=";")
    df = df.groupby(np.arange(len(df)) // 800).mean()

    df = df.round({"t": 1, "db": 7})
    if rescale:
        tmp_df = df.drop("t", axis=1)
        df_norm = (tmp_df - tmp_df.min()) / (tmp_df.max() - tmp_df.min())

        df["db"] = df_norm["db"]

    df.to_csv(PATH + "filtered_" + filename + ".csv", index=False, decimal=",", sep=";")

    if createPlot:
        fig = plt.figure(figsize=(13, 10))
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
        sns.scatterplot(
            x="t",
            y="db",
            data=df,
        )

        # plt.show()
        plt.savefig(PATH + filename + ".png")

    return df
