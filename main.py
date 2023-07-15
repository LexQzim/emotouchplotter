import pandaReader as pr
import seabornDrawer as sd
import os
import sys

# this is a list for four file sessions.
# Update this list with your names
# Keep in mind that you also need to update the list symbol_used, noise_versions and titles
# all this lists need the same amount of elements
# please pay attention to spacebars. Replace them with underscore (_)
fileNames = ["emoTouch_aus_einschleichend_MIT_aufforderung",
             "emoTouch_pretest_ein_ausschleichend_MIT_aufforderung",
             "emoTouch_pretest_ein_ausschleichend_ohne_aufforderung",
             "emoTouch_aus_einschleichend_ohne_neu"]

# you can update this ending if it doesn't fits your needs
# these are the default endings wich are added to all emotouch .csv-files
timeline_data_ending = "_timeline_data_v1.6.1"
session_metadata_ending = "_session_metadata_v1.6.1"
version_1_7_ending = "_version1.7_(100_ms)"

# This is a list of all soSci Survey Ids which you want to have in your results. 
# You need to update this list for your needs
needed_ids = [441, 442, 447, 453, 475, 477, 486, 487, 490, 494, 498, 503, 520, 524, 530, 531, 532, 534, 535, 538, 539, 545, 547, 550, 552, 560, 565, 569, 571, 574, 575, 576, 584, 585, 593, 595, 611, 615, 616, 621, 622, 635, 659, 664, 667, 676, 677,
              681, 688, 693, 700, 701, 705, 721, 726, 728, 746, 748, 756, 761, 766, 767, 770, 773, 780, 781, 785, 788, 798, 808, 811, 812, 814, 823, 839, 845, 847, 859, 866, 867, 868, 878, 880, 883, 887, 889, 890, 891, 893, 906, 907, 912, 913, 917, 931, 937, 948]

# this is a very specific case which you are generaly don't need. 
# Just type False for the amount of your used files
symbol_used = [True, True, False, False]

# there a three different types
# noise version 0 = no noise
# noise version 1 = fade in and then fade out
# noise version 2 = fade out and then fade int
noise_versions = [2,1,1,2]

# update for each file type your plot titles
titles = ["Versuch:  aus- und einschleichendes Rauschen mit Aufforderung, ID: ",
           "Versuch: ein- und ausschleichendes Rauschen mit Aufforderung, ID: ",
           "Versuch: ein- und ausschleichendes Rauschen ohne Aufforderung, ID: ",
           "Versuch: aus- und einschleichendes Rauschen ohne Aufforderung, ID: "]


def call_operations_1(filename, delimiter, title, draw_signal_boxes, draw_noise, doExtra = False):
    '''
    This method can do everything what you want for one session
    :filename: this is the name of the session
    :delimiter: this is the .csv delimiter. You set this emotouch before you load the data
    :draw_signal_boxes: when True then it will draw yellow boxes
    :draw_noise: You can choose a noise type between 0, 1 and 2
    :doExtra: If True, then this will also find last ticks and calc mean median and standard deviation and reorder the list
    '''
    timeline_df = pr.read_and_merge_timeline_data(filename+timeline_data_ending, filename+session_metadata_ending, delimiter, needed_ids, output_filename=filename)
    sd.create_and_save_scatter_plot(timeline_df, title, output_filename=filename, draw_noise=draw_noise, draw_signal_boxes=draw_signal_boxes)
    if doExtra:
        reorderd_timeline_data = pr.reorder_timeline_data(timeline_df)
        pr.find_last_ticks_and_save_to_csv(reorderd_timeline_data, filename)
        pr.calc_mean_median_stdev(reorderd_timeline_data, filename)


def call_operations_2(filename_origin, filename_resampled, delimiter_origin, delimiter_resampled, title, draw_signal_boxes, draw_noise):
    timeline_origin_df = pr.read_and_merge_timeline_data(filename_origin+timeline_data_ending, filename_origin+session_metadata_ending, delimiter_origin, needed_ids)
    timeline_resampled_df = pr.read_and_merge_timeline_data(filename_resampled+timeline_data_ending, filename_resampled+session_metadata_ending, delimiter_resampled, needed_ids)

    sd.create_and_save_line_and_scatter_plot(timeline_origin_df, timeline_resampled_df, title, output_filename=filename_origin, draw_noise=draw_noise, draw_signal_boxes=draw_signal_boxes)

if __name__ == "__main__":
    path = "data/origin/"
    if not os.path.exists(path):
        os.makedirs(path)

    if len(os.listdir(path)) == 0:
        print("You need to place first your .csv files into this directory.")
        sys.exit()

    for i in range(len(fileNames)):

        # you can outcomment the operations with #

        # original data
        call_operations_1(filename=fileNames[i], delimiter=";", title=titles[i], draw_signal_boxes=symbol_used[i], draw_noise=noise_versions[i])

        # resampled data (100 ms)
        # call_operations_1(filename=fileNames[i]+version_1_7_ending, title=titles[i], delimiter=";", draw_signal_boxes=symbol_used[i], draw_noise=noise_versions[i], doExtra=True)

        # plot both original and resampled data in one image
        # call_operations_2(filename_origin=fileNames[i], filename_resampled=fileNames[i]+version_1_7_ending, delimiter_origin=";", title=titles[i], delimiter_resampled=";", draw_signal_boxes=symbol_used[i], draw_noise=noise_versions[i])





    # timeline_origin_df = pr.read_and_merge_timeline_data("test_timeline_data", "test_session_metadata", delimiter="\t", needed_ids=needed_ids, output_filename="filtered_testoutput_origin")
    # timeline_resampled_df = pr.read_and_merge_timeline_data("test_resampled_timeline_data", "test_resampled_session_metadata", delimiter=";", needed_ids=needed_ids, output_filename="filtered_testoutput_resampled")
    # sd.create_and_save_scatter_plot(timeline_origin_df, title="SoSci Survey Id: ", output_filename="test_plot", draw_noise=1, draw_signal_boxes=True, testPlot=False)
    # sd.create_and_save_line_and_scatter_plot(timeline_origin_df, timeline_resampled_df, title="SoSci Survey Id: ", output_filename="test_plot", draw_noise=1, draw_signal_boxes=True, testPlot=False)
    # sd.create_and_save_scatter_plot(timeline_resampled_df, title="SoSci Survey Id: ", output_filename="test_plot", draw_noise=1, draw_signal_boxes=True, testPlot=False, dataResampled=True)
    # reorderd_timeline_data = pr.reorder_timeline_data(timeline_resampled_df)
    # pr.find_last_ticks_and_save_to_csv(reorderd_timeline_data, "test")
    # reorderd_timeline_data = pr.calc_mean_median_stdev(reorderd_timeline_data, "test")

    # sd.create_error_timeline_plot(reorderd_timeline_data, noise_version = 1)