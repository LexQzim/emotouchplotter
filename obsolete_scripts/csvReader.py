
import csv
import statistics

type_timeline_data = "_timeline_data_v1.6.1"
type_object_meta_data = "_object_metadata_v1.6.1"
type_session_meta_data = "_session_metadata_v1.6.1"
type_last_value_timeline_data = "_last_value_timeline_data_v1.6.1"

refactored_100ms = "_version1.7_(100_ms)"

# obsolete

def read_resampled_and_reorder_csv(filename, needed_ids):
    session_data = {}
    with open("data/100ms/"+filename + refactored_100ms + type_session_meta_data+".csv", newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=';')
        line_count = 0

        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue

            if (row[5] != ""):
                session_data[row[0]] = row[5]

    timeline_data = {}
    time=[]

    soCi_ids=[]

    meanArray=[]
    stdevArray=[]

    with open("data/100ms/"+filename +refactored_100ms + type_timeline_data+".csv", newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=';')

        firstLine = True
        for row in csv_reader:
            if firstLine:
                firstLine = False
                continue

            obj_id = row[0]
            rel_time = int(row[6])
            type_ = row[7]
            value = row[8]

            if obj_id in session_data:
                if int(session_data[obj_id]) in needed_ids:
                    soCi_Id = int(session_data[obj_id])
                    if (rel_time >= 0 and value != "" and type_ == "TICKCHANGE"):
                        if(not soCi_Id in soCi_ids):
                            soCi_ids.append(soCi_Id)

                        if(not rel_time in time):
                            time.append(rel_time)

                        if (timeline_data.get(rel_time) is None):
                            timeline_data[rel_time] = {}

                        if (type_ == "TICKCHANGE"):
                            timeline_data[rel_time][soCi_Id] =float(value)

    time.sort()
    soCi_ids.sort()
    soCi_ids.append("mean")
    soCi_ids.append("median")
    soCi_ids.append("stdev")

    for rel_time in timeline_data:
        values = []
        counter = 0
        for soCi_id in soCi_ids:
            if (not timeline_data[rel_time].get(soCi_id) is None):
                values.append(timeline_data[rel_time][soCi_id])
                counter += 1

        if(len(values) > 0):
            timeline_data[rel_time]["mean"] = statistics.mean(values)
            timeline_data[rel_time]["median"] = statistics.median(values)
            if (len(values) > 1):
                timeline_data[rel_time]["stdev"] = statistics.stdev(values)
            else:
                timeline_data[rel_time]["stdev"] = 0
        else:
            timeline_data[rel_time]["mean"] = -0.01
            timeline_data[rel_time]["median"] = -0.01
            timeline_data[rel_time]["stdev"] = 0

        meanArray.append(timeline_data[rel_time]["median"])
        stdevArray.append(timeline_data[rel_time]["stdev"])

    createErrorTimeLinePlot([meanArray, time, stdevArray])

    header = ["time"] + soCi_ids

    with open("data/refactored/"+filename +refactored_100ms +'.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

        for rel_time in timeline_data:
            result = [rel_time]
            for soCi_id in soCi_ids:
                if (timeline_data[rel_time].get(soCi_id) is None):
                    result += ['']
                else:
                    result += [timeline_data[rel_time][soCi_id]]

            writer.writerow(result)

    return timeline_data

def read_timeline_data(filename):
    timeline_data = {}
    # with open("data/"+filename+type_timeline_data+".csv", newline='') as csvfile:
    with open("data/"+filename, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=';')
        line_count = 0
        
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue

            if (timeline_data.get(row[0]) is None):
                timeline_data[row[0]] = []

            timeline_data[row[0]].append([row[8], row[9], row[6], row[7]])

    return timeline_data

def read_timeline_data_simple(filename):
    x = []
    t = []
    type=[]
    id = []
    with open("data/"+filename+type_timeline_data+".csv", newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter='\t')
        line_count = 0

        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            if(row[4] != "" and float(row[4]) >= 0 and float(row[4]) <= 1 ):
                x.append(float(row[4]))
                type.append(row[6])
                t.append(float(row[7])/1000)
                id.append(int(row[1]))

    return [x,t,type, id]

def read_session_data(filename):
    session_data = {}
    with open("data/"+filename+type_session_meta_data+".csv", newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter='\t')
        line_count = 0

        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue

            if (row[5] != ""):
                session_data[row[0]] = row[5]

    return session_data


def create_csv(timeline_data, session_data, filename, needed_ids):
    with open(filename+'.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["emotouchid_id", "sosci_survey_id", "created_at", "value", "type", "created_at_relative"])

        for key in timeline_data:
            if key in session_data:
                if int(session_data[key]) in needed_ids:
                    for row in timeline_data[key]:
                        writer.writerow([key, session_data[key], row[0], row[1], row[2], row[3]])

