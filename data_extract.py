import os
import sys

def extract_file_names(path):
    res = []
    with open(path, "r") as f:
        for line in f.readlines():
            line = line.strip('\n')
            res.append(line)

    return res

def extract_instance(path):
    res = []
    with open(path, "r") as f:
        for line in f.readlines():
            line = line.strip('\n')
            res.append(line.split())

    return res

class Instance:
    def __init__(self):
        self.job_num = 0
        self.stage_num = 0
        self.machine_num = []
        self.process_time = []
        self.due_date = []
        self.earliness_window = []
        self.tardiness_window = []
        self.earliness_weights = []
        self.tardiness_weights = []
        self.lower_bound_cmax = []

        self.T = 0.0
        self.R = 0.0
        self.W = 0.0

    def generate_ins(self, ins_name, ins_data):
        # extract info from file name
        ins_name = ins_name.strip('.txt')
        pos = ins_name.rfind("Instance_")
        ins_name = ins_name[(pos+9):]
        ins_name = ins_name.replace(",", ".")
        name_info = ins_name.split('_')

        self.job_num = int(name_info[0])
        self.stage_num = int(name_info[1])
        self.machine_num = int(name_info[2])
        self.T = float(name_info[3])
        self.R = float(name_info[4])
        self.W = float(name_info[5])

        # extract info from data in file
        # process time
        for i in range(2, 2+self.job_num):
            p_time = []
            for j in range(self.stage_num):
                p_time.append(float(ins_data[i][2*j+1]))
            self.process_time.append(p_time)

        # lower bound cmax
        row = 2+self.job_num
        self.lower_bound_cmax = float(ins_data[row][1])

        # due date, due window weight
        start = 2 + self.job_num + 2
        end = start + self.job_num
        for i in range(start, end):
            self.due_date.append(float(ins_data[i][1]))
            self.earliness_weights.append(float(ins_data[i][2]))
            self.tardiness_weights.append(float(ins_data[i][3]))

        # window
        start = end + 1
        end = start + self.job_num
        for i in range(start, end):
            self.earliness_window.append(float(ins_data[i][0]))
            self.tardiness_window.append(float(ins_data[i][1]))


# extract ins data
def extract_data():
    folder = "HFSDDW/smallCalibration/"
    file_name_path = folder + "InstanceName.txt"
    ins_names = extract_file_names(file_name_path)

    # extract instance data
    ins_data_set = []
    for ins_name in ins_names:
        ins_data = extract_instance(folder + ins_name)
        ins_data_set.append(ins_data)

    # generate instance
    ins_num = len(ins_names)
    res = []
    for i in range(ins_num):
        ins = Instance()
        ins.generate_ins(ins_names[i], ins_data_set[i])
        res.append(ins)

    return res

if __name__ == "__main__":
    ins_set = extract_data()



