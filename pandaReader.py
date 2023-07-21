import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.options.display.max_rows = 9999


def read_and_merge_timeline_data(
    timeline_filename, session_data_filename, delimiter, needed_ids, output_filename=""
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
    # drop rows with nan values
    new_timeline_df = new_timeline_df.dropna()
    # set type of each column for savety reasons
    new_timeline_df = new_timeline_df.astype(
        {
            "session_id": "int16",
            "x": "float32",
            "created_at_relative": "float32",
            "type": "str",
            "s1": "int16",
        }
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
        new_timeline_df[new_timeline_df["type"] != "TICKCHANGE"].index
    )
    # drop dupcliated column
    new_timeline_df = new_timeline_df.drop(columns="id")
    # rename col s1 to soSci_survey_Id
    new_timeline_df = new_timeline_df.rename(columns={"s1": "soSci_survey_Id"})
    # select only specific soci survey ids
    new_timeline_df = new_timeline_df.drop(
        new_timeline_df[~new_timeline_df["soSci_survey_Id"].isin(needed_ids)].index
    )

    # uncomment to get a tablepreview
    # print(new_timeline_df.head())

    # check if path exists. if not then create a new one
    path = "data/clean_and_merged/"
    if not os.path.exists(path):
        os.makedirs(path)

    # create csv of filtered data
    if output_filename != "":
        new_timeline_df.to_csv(path + output_filename + ".csv", index=False)

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

    # show count of rows
    # print(len(timeline_df))
    # show preview of first 5 rows
    # print(timeline_df.head())
    # show last index
    # print(timeline_df.index[-1])

    return timeline_df


def calc_mean_median_stdev(timeline_df: pd.DataFrame, output_filename=""):
    timeline_df["mean"] = timeline_df.mean(axis=1)
    timeline_df["median"] = timeline_df.median(axis=1)
    timeline_df["stdev"] = timeline_df.std(axis=1)

    # reorder header level and give it a propper namer
    timeline_df = timeline_df.droplevel(axis=1, level=0)
    header = timeline_df.columns.to_list()
    header[-1] = "stdev"
    header[-2] = "median"
    header[-3] = "mean"
    timeline_df.columns = header

    # save file
    path = "data/refactored/"
    if not os.path.exists(path):
        os.makedirs(path)

    if not output_filename == "":
        timeline_df.to_csv(path + output_filename + ".csv")

    return timeline_df


def find_last_ticks_and_save_to_csv(timeline_df: pd.DataFrame, output_filename=""):
    # get all last valid ticks
    last_valid_ticks = timeline_df.apply(pd.Series.last_valid_index)
    # change type
    last_valid_ticks = pd.Series.to_frame(last_valid_ticks)
    # rename column and reset index for clear naming
    last_valid_ticks.rename(columns={0: "timestamp"}, inplace=True)
    last_valid_ticks = last_valid_ticks.reset_index()
    last_valid_ticks = last_valid_ticks.drop(columns="level_0")

    # check if path exists. if not then create a new one
    path = "data/lastTicks/"
    if not os.path.exists(path):
        os.makedirs(path)

    # create csv of filtered data
    if not output_filename == "":
        last_valid_ticks.to_csv(path + output_filename + ".csv", index=False)

    # comment this out to get a preview of found data
    # sns.scatterplot(y='soSci_survey_Id',x='timestamp', data=last_valid_ticks, edgecolor = "green", color = "green", alpha = 0.4)
    # plt.show()
