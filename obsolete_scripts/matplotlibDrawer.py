import matplotlib.pyplot as plt
import os
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection

def createPlot(timeline_data, session_data, filename, needed_ids, symbole_time, draw_symbol):

    # for key in timeline_data:
    #     if key in session_data:
    #         if int(session_data[key]) in needed_ids:
    #             id = session_data[key]
                id = "1"
                key = "5029"
                t = []
                y = []

                last_y = 51
                
                count_changes = 0
                prev_t = -10000
                

                for row in timeline_data[key]:
                    print(row)

                    if (row[2] == "PLAY"):
                        t.append(int(row[3])/1000)
                        y.append(0.51)
                        prev_t = int(row[3])

                    if (row[2] == "TICKCHANGE"):
                        t.append(int(row[3])/1000)
                        y.append(float(row[1]))
                        last_y = float(row[1])
                        
                        
                        if ((int(row[3])-prev_t) > 100):
                            count_changes +=1
                        
                        prev_t = int(row[3])


                print(count_changes)
                # t.append(int(timeline_data[key][-1][3])/1000)
                # y.append(last_y)

                fig = plt.figure(figsize=(13, 10))
                ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

                plt.ylim(0, 1.1)
                maxX = 69
                if max(t) > maxX:
                    plt.xlim(0, max(t))
                    plt.vlines(maxX, 0, 1, colors="k", linestyles="dashed")
                    maxX = max(t)
                else:
                    plt.xlim(0, maxX)

                plt.grid(color="gray", which="both")

                if "ein_ausschleichend" in filename:
                    # ein_ausschleichend
                    plt.plot([11, 39], [0, 1], color="silver")
                    plt.fill_between([11, 39], [0, 1], alpha=0.4, facecolor="silver")
                    plt.plot([39, 67], [1, 0], color="silver")
                    plt.fill_between([39, 67], [1, 0], alpha=0.4, facecolor="silver")

                elif "aus_einschleichend" in filename:
                    # aus_einschleichend
                    plt.plot([0, 0.85], [0, 1], color="silver")
                    plt.fill_between([0, 0.85], [0, 1], alpha=0.4, facecolor="silver")
                    plt.plot([0.85, 30], [1, 0], color="silver")
                    plt.fill_between([0.85, 30], [1, 0], alpha=0.4, facecolor="silver")
                    plt.plot([37.6, 68], [0, 1], color="silver")
                    plt.fill_between([37.6, 68], [0, 1], alpha=0.4, facecolor="silver")

                    # newy = np.polyfit([37.6,68], np.log([0,1]), 1)
                    # print(newy)

                    # plt.plot([37.6,68], newy, color="r")
                    # popt, pcov = curve_fit(lambda t, a, b, c: a * np.exp(b * t) + c, [0.85, 20, 30], [1,0])
                    # a = popt[0]
                    # b = popt[1]
                    # c = popt[2]
                    # print(a)

                if draw_symbol:
                    rects = []
                    for time in symbole_time:
                        signal = patches.Rectangle((time, -0.1), 3, 1.2)
                        rects.append(signal)

                    pc = PatchCollection(rects, facecolor='g', alpha=0.3)

                    ax.add_collection(pc)

                plt.plot(t, y, marker='.')

                plt.ylabel('Wert')
                plt.xlabel('Zeit (sec)')
                plt.title(filename + ": " + id + " (Anzahl: " + str(len(timeline_data[key]))+")")

                # print(t)
                # print(min(t))
                # print(max(t))
                plt.show()

                # if not os.path.exists("plots/"+filename):
                #     os.makedirs("plots/"+filename)

                # plt.savefig("plots/"+filename+"/"+id+".png")
                # # plt.savefig("plots/"+filename+"/"+id+".svg")
                # plt.clf()
                # plt.close()


def createMassPlot(timeline_data, session_data, filename, needed_ids, symbole_time, draw_symbol):

    fig = plt.figure(figsize=(13, 10))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

    plt.ylim(0, 1.1)

    plt.grid(color="gray", which="both")

    if "ein_ausschleichend" in filename:
        # ein_ausschleichend
        plt.plot([11, 39], [0, 1], color="silver")
        plt.fill_between([11, 39], [0, 1], alpha=0.4, facecolor="silver")
        plt.plot([39, 67], [1, 0], color="silver")
        plt.fill_between([39, 67], [1, 0], alpha=0.4, facecolor="silver")

    elif "aus_einschleichend" in filename:
        # aus_einschleichend
        plt.plot([0, 0.85], [0, 1], color="silver")
        plt.fill_between([0, 0.85], [0, 1], alpha=0.4, facecolor="silver")
        plt.plot([0.85, 30], [1, 0], color="silver")
        plt.fill_between([0.85, 30], [1, 0], alpha=0.4, facecolor="silver")
        plt.plot([37.6, 68], [0, 1], color="silver")
        plt.fill_between([37.6, 68], [0, 1], alpha=0.4, facecolor="silver")

    if draw_symbol:
        rects = []
        for time in symbole_time:
            signal = patches.Rectangle((time, -0.1), 3, 1.2)
            rects.append(signal)

        pc = PatchCollection(rects, facecolor='g', alpha=0.3)

        ax.add_collection(pc)

    maxX = 69

    for key in timeline_data:
        if key in session_data:
            if int(session_data[key]) in needed_ids:
                t = []
                y = []

                last_y = 51

                for row in timeline_data[key]:

                    if (row[2] == "PLAY"):
                        t.append(int(row[3])/1000)
                        y.append(0.51)

                    if (row[2] == "TICKCHANGE"):
                        t.append(int(row[3])/1000)
                        y.append(float(row[1]))
                        last_y = float(row[1])

                t.append(int(timeline_data[key][-1][3])/1000)
                y.append(last_y)

                if max(t) > maxX:
                    plt.xlim(0, max(t))
                    plt.vlines(maxX, 0, 1, colors="k", linestyles="dashed")
                    maxX = max(t)
                else:
                    plt.xlim(0, maxX)

                plt.plot(t, y, marker='.', linestyle='None',)

    plt.ylabel('Wert')
    plt.xlabel('Zeit (sec)')
    plt.title(filename)

    # print(t)
    # print(min(t))
    # print(max(t))
    plt.show()

    # if not os.path.exists("plots/"+filename):
    #     os.makedirs("plots/"+filename)

    # plt.savefig("plots/"+filename+"/"+id+".png")
    # plt.savefig("plots/"+filename+"/"+id+".svg")
    plt.clf()
    plt.close()