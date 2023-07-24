import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import seabornDrawer as sd
import scipy.optimize as sio

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
    timeline_df = timeline_df.droplevel(axis=1, level=0)
    timeline_df = timeline_df.reset_index()
    timeline_df = timeline_df.rename(columns={"soSci_survey_Id": "index"})

    # show count of rows
    # print(len(timeline_df))
    # show preview of first 5 rows
    # print(timeline_df.head())
    # show last index
    # print(timeline_df.index[-1])

    # print(timeline_df["created_at_relative"].max())
    # print(timeline_df[447].min())
    # print(timeline_df[447].max())

    return timeline_df


def calc_mean_median_stdev(timeline_df: pd.DataFrame, output_filename=""):
    timeline_df["mean"] = timeline_df.mean(axis=1)
    timeline_df["median"] = timeline_df.median(axis=1)
    timeline_df["stdev"] = timeline_df.std(axis=1)

    # reorder header level and give it a propper namer
    # timeline_df = timeline_df.droplevel(axis=1, level=0)
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
        timeline_df.to_csv(path + output_filename + ".csv", index=False)
    return timeline_df


def find_last_ticks_and_save_to_csv(timeline_df: pd.DataFrame, output_filename=""):
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
        last_valid_ticks.to_csv(path + output_filename + ".csv")

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
        new_df.to_csv(PATH + output_filename + ".csv", index=False)


def extract_noise_values(filename):
    df = pd.read_csv(filename, sep="\t", low_memory=False)
    df = df.drop(df[df["db_l"] == "[-inf]"].index)
    df = df.drop(df[df["db_r"] == "[-inf]"].index)
    df = df.drop(df[df["db_l"] == "[inf]"].index)
    df = df.drop(df[df["db_r"] == "[inf]"].index)

    df = df.astype(
        {
            "t_l": "float32",
            "db_l": "float32",
            "t_r": "float32",
            "db_r": "float32",
        }
    )

    noise = [(i + j) / 2 for i, j in zip(df["db_l"], df["db_r"])]

    for i in range(10):
        del noise[-1]

    noise = [x * -1 for x in noise]

    return noise


def combine_noise_values(filenames: list):
    noise = []
    for filename in filenames:
        noise += extract_noise_values(filename)

    return noise


def read_noise_text_calc_mean(noises: list, starttimes: list):
    combined_noise = [0] * int((starttimes[0] * 10))

    time = np.linspace(0, 68, 680)
    n = 4800

    for i, noise in enumerate(noises):
        calced_mean_100ms = [
            sum(noise[i : i + n]) // n for i in range(0, len(noise), n)
        ]
        calced_mean_100ms = [
            scale(x, (min(calced_mean_100ms), max(calced_mean_100ms)))
            for x in calced_mean_100ms
        ]

        # calced_mean_100ms = list(map(abs, calced_mean_100ms))

        # calced_mean_100ms = [x * -1 for x in calced_mean_100ms]

        # calced_mean_100ms = [
        #     float(i) / max(calced_mean_100ms) for i in calced_mean_100ms
        # ]

        # calced_mean_100ms.reverse()

        combined_noise = combined_noise + calced_mean_100ms

        if i < len(starttimes) - 1:
            if len(combined_noise) != starttimes[i + 1]:
                next_start_absolut = starttimes[i + 1] * 10
                next_start_relative = next_start_absolut - len(combined_noise)
                combined_noise = combined_noise + [0] * int(next_start_relative)

    # noise = [float(i) / max(noise) for i in noise]

    # noise = [
    #     float(i) + max_neg_noise for i in noise
    # ]
    next_start_relative = len(time) - len(combined_noise)
    combined_noise = combined_noise + [0] * next_start_relative

    # # time = range(0, len(list2)) / 10
    # time = np.linspace(0, len(list2), len(list2))
    # print(time)

    new_df = pd.DataFrame([time, combined_noise], index=["x", "y"]).T
    # print(new_df.head())
    fig = plt.figure(figsize=(13, 10))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    sns.scatterplot(
        x="x",
        y="y",
        data=new_df,
    )

    plt.show()


def f(x, A, B):
    return A * np.exp(B * x) + A


def scale(x, srcRange):
    return (x - srcRange[0]) / (srcRange[1] - srcRange[0])


def read_noise_txt(filename, secondFilename=""):
    data = pd.read_csv(filename, sep="\t")
    data = data.drop(data[data["db_l"] == "[-inf]"].index)
    data = data.astype(
        {
            "t_l": "float32",
            "db_l": "float32",
            "t_r": "float32",
            "db_r": "float32",
        }
    )

    if secondFilename != "":
        data2 = pd.read_csv(secondFilename, sep="\t")
        data2 = data2.drop(data2[data2["db_l"] == "[-inf]"].index)
        data2 = data2.astype(
            {
                "t_l": "float32",
                "db_l": "float32",
                "t_r": "float32",
                "db_r": "float32",
            }
        )

        # print(len(data["db_l"]))
        y1 = data["db_l"].to_list()
        del y1[::2]
        y2 = data2["db_l"].to_list()
        del y2[::2]
        # print(len(data2["db_l"]))
        y_values = y1 + y2
        x_values = [0.00002, 0.00006]
        for i in range(len(y_values)):
            if i < 2:
                continue
            x_values.append(x_values[i - 1] + 0.00004)

        print(len(x_values))
        # y_values = y_values * (-1)
        print(len(y_values))

        dict = {"x": x_values, "y": y_values}

        # df = pd.DataFrame(dict)
        df = pd.DataFrame([x_values, y_values], index=["x", "y"]).T
        df["y"] = df["y"] * (-1)

        # print(df.head())

        fig = plt.figure(figsize=(13, 10))
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
        sns.scatterplot(
            x="x",
            y="y",
            data=df,
        )
        plt.savefig(filename + ".png")

    else:
        data["db_l"] = data["db_l"] * (-1)
        # data["t_l"] = data["t_l"] + 11

        # calculate parameter for polinomial function of given power
        # p = np.polyfit(x=data["t_l"], y=data["db_l"], deg=2)

        # calculate new values for fitted curve
        # xf = np.linspace(11, 23, 50)
        # yf = sd._polynomial_function(p, xf, 2)

        # yf -= yf[0]

        # if not fadeIn:
        # yf = sio.curve_fit(f, data["t_l"], data["db_l"])
        # yf -= yf[0]
        # yf = -np.flip(yf)

        # polynomDf = pd.DataFrame(data={"x": data["t_l"], "y": yf})
        # yf = f(data["t_l"], *yf[0])
        # print(yf[-1])
        # yf = -np.flip(yf)
        # yf -= yf[-1]

        # plt.plot(data["t_l"], yf)

        fig = plt.figure(figsize=(13, 10))
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
        sns.scatterplot(
            x="t_l",
            y="db_l",
            data=data,
        )
        # sns.lineplot(
        #     x="x",
        #     y="y",
        #     data=polynomDf,
        # )

        # plt.show()
        plt.savefig(filename + ".png")
