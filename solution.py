import data_extract
import sys
import copy


class Task:
    def __init__(self, type='idle', job_id=0, start_time=0.0, finish_time=0.0):
        self.type = type
        self.job_id = job_id
        self.start_time = start_time
        self.finish_time = finish_time


class Solution:
    def __init__(self, ins):
        self.ins = ins
        self.eval = 0.0
        self.sequence = [i for i in range(ins.job_num)]

        self.tasks = []
        for i in range(ins.stage_num):
            stage_tasks = []
            for j in range(ins.job_num):
                stage_tasks.append(Task('real', j, 0.0, 0.0))
            self.tasks.append(stage_tasks)

        self.sol = []  # task sequence on each machine
        for i in range(ins.stage_num):
            stage_sol = []
            for j in range(ins.machine_num):
                stage_sol.append([])
            self.sol.append(stage_sol)

    # using first available machine rule to generate sol
    def fam(self):
        seq = copy.deepcopy(self.sequence)
        for i in range(self.ins.stage_num):
            self.fam_single_stage(i, seq)
            seq = sorted(seq, key=lambda x: (self.tasks[i][x].finish_time, self.ins.tardiness_window[x]))

    # calc each stage
    def fam_single_stage(self, stage, job_seq):
        for j in job_seq:
            index = 0
            min_avail_time = float('inf')
            for k in range(self.ins.machine_num):
                if stage == 0:
                    if len(self.sol[stage][k]) == 0:
                        index = k
                        min_avail_time = 0.0
                        break

                    avail_time = self.tasks[stage][self.sol[stage][k][-1]].finish_time
                    if avail_time < min_avail_time:
                        index = k
                        min_avail_time = avail_time

                else:
                    if len(self.sol[stage][k]) == 0:
                        index = k
                        min_avail_time = self.tasks[stage - 1][j].finish_time
                        break

                    avail_time = max(self.tasks[stage][self.sol[stage][k][-1]].finish_time,
                                     self.tasks[stage - 1][j].finish_time)
                    if avail_time < min_avail_time:
                        index = k
                        min_avail_time = avail_time

            self.sol[stage][index].append(j)
            self.tasks[stage][j] = Task('real', j, min_avail_time, min_avail_time + self.ins.process_time[stage][j])

    # insert idle time task to improve solution
    def insert_idle_time(self):
        for i in range(self.ins.machine_num):
            sm = []
            job_num = len(self.sol[0][i])
            j = job_num - 1
            delta2 = 0.0
            while j >= 0:
                # construct sm
                sm.clear()
                sm.append(j)
                for k in range(j, job_num - 1):
                    job_id1 = self.sol[0][i][k]
                    job_id2 = self.sol[0][i][k + 1]
                    if self.tasks[0][job_id1].finish_time >= self.tasks[0][job_id2].start_time:
                        sm.append(k + 1)
                    else:
                        break

                # calc delta2
                if sm[-1] < job_num - 1:
                    job_id1 = self.sol[0][i][sm[-1]]
                    job_id2 = self.sol[0][i][sm[-1] + 1]
                    delta2 = self.tasks[0][job_id2].start_time - self.tasks[0][job_id1].finish_time
                else:
                    delta2 = float('inf')

                # generate Se, Sd, St from Sm
                se, st, sd = self.generate_se_st_sd(0, i, sm)
                sum_se = 0.0
                min_earliness = float('inf')
                for index in se:
                    job_id = self.sol[0][i][index]
                    sum_se += self.ins.earliness_weights[job_id]

                    earliness = self.ins.earliness_window[job_id] - self.tasks[-1][job_id].finish_time
                    min_earliness = min(earliness, min_earliness)

                sum_st = 0.0
                for index in st:
                    job_id = self.sol[0][i][index]
                    sum_st += self.ins.earliness_weights[job_id]

                min_due_time = float('inf')
                for index in sd:
                    job_id = self.sol[0][i][index]

                    due_time = self.ins.tardiness_window[job_id] - self.tasks[-1][job_id].finish_time
                    min_due_time = min(due_time, min_due_time)

                delta1 = min(min_earliness, min_due_time)
                delta = min(delta1, delta2)
                if sum_se > sum_st and delta > 0:
                    self.insert_idle_time_update(0, i, sm, delta)
                else:
                    j = j - 1


    def generate_se_st_sd(self, stage, machine, sm):
        se = []
        st = []
        sd = []
        for index in sm:
            job_id = self.sol[stage][machine][index]
            if self.tasks[-1][job_id].finish_time < self.ins.earliness_window[job_id]:
                se.append(index)
            elif self.tasks[-1][job_id].finish_time > self.ins.tardiness_window[job_id]:
                st.append(index)
            else:
                sd.append(index)

        return se, st, sd

    def insert_idle_time_update(self, stage, machine, sm, idle_time):
        for index in sm:
            job_id = self.sol[stage][machine][index]
            self.tasks[stage][job_id].start_time += idle_time
            self.tasks[stage][job_id].finish_time += idle_time

    # calc the evaluation
    def calc_eval(self):

        return 0.0


if __name__ == "__main__":
    # test fam func
    ins = data_extract.Instance()
    ins.job_num = 5
    ins.stage_num = 2
    ins.machine_num = 2
    ins.process_time = [[4, 3, 6, 2, 1], [5, 4, 1, 1, 4]]
    ins.earliness_window = [8, 7, 10, 7, 9]
    ins.tardiness_window = [10, 9, 11, 10, 11]
    ins.earliness_weights = [1, 2, 1, 3, 1]
    ins.tardiness_weights = [2, 1, 2, 1, 3]

    sol = Solution(ins)
    sol.sequence = [0, 1, 2, 3, 4]
    sol.fam()

    # test insert_idle_time func
    ins1 = data_extract.Instance()
    ins1.job_num = 8
    ins1.stage_num = 1
    ins1.machine_num = 1
    ins1.process_time = [5, 4, 4, 6, 7, 2, 6, 4]
    ins1.earliness_window = [62, 67, 70, 74, 79, 88, 93, 97]
    ins1.tardiness_window = [64, 68, 72, 76, 81, 90, 95, 99]
    ins1.earliness_weights = [1, 2, 1, 3, 1, 2, 1, 4]
    ins1.tardiness_weights = [2, 1, 2, 1, 2, 1, 2, 3]
    sol1 = Solution(ins1)
    sol1.sol[0][0] = [0, 1, 2, 3, 4, 5, 6, 7]
    sol1.tasks[0][0] = Task('real', 0, 56, 61)
    sol1.tasks[0][1] = Task('real', 1, 61, 65)
    sol1.tasks[0][2] = Task('real', 2, 65, 69)
    sol1.tasks[0][3] = Task('real', 3, 69, 75)
    sol1.tasks[0][4] = Task('real', 4, 75, 82)
    sol1.tasks[0][5] = Task('real', 5, 84, 86)
    sol1.tasks[0][6] = Task('real', 6, 86, 92)
    sol1.tasks[0][7] = Task('real', 7, 93, 97)

    sol1.insert_idle_time()
    print("end")
