import data_extract
import solution

class ConstructHeuristic:
    def __init__(self, sol):
        self.ins = sol.ins
        self.sol = sol

    # sort the sol under earliest due date order
    def edd(self):
        self.sol.sequence = sorted(self.sol.sequence, key=lambda x: self.ins.due_date[x])


    # sort the solution under tardiness - processing_time
    def lsl(self):
        self.sol.sequence = sorted(self.sol.sequence, key=lambda x: self.ins.tardiness_window[x] - self.ins.process_time[-1][x])

    # sort the solution under tardiness - sum(processing_time)
    def osl(self):
        process_time_sum = [0]*self.ins.job_num
        for i in range(self.ins.job_num):
            sum = 0
            for j in range(self.ins.stage_num):
                sum += self.ins.process_time[j][i]
            process_time_sum[i] = sum

        self.sol.sequence = sorted(self.sol.sequence, key=lambda x: self.ins.tardiness_window[x] - process_time_sum[x])


class ImproveHeuristics:
    def __init__(self, sol):
        self.ins = sol.ins
        self.sol = sol

    def VND(self):
        pass

    def limited_neighbors(self):
        pass

class IteratedGreedy:
    def __init__(self, sol):
        self.ins = sol.ins
        self.sol = sol

    def construction(self):
        pass

    def reconstruction(self):
        pass


class MainLoop:
    def __init__(self, sol):
        self.ins = sol.ins
        self.sol = sol

    def algorithm(self):
        pass

    def show_result(self):
        pass


if __name__ == "__main__":
    # test fam func
    ins = data_extract.Instance()
    ins.job_num = 5
    ins.stage_num = 2
    ins.machine_num = 2
    ins.process_time = [[4, 3, 6, 2, 1], [5, 4, 1, 1, 4]]
    ins.earliness_window = [8, 7, 10, 7, 9]
    ins.tardiness_window = [10, 9, 11, 10, 11]
    ins.due_date = [9, 8, 10, 8, 11]
    ins.earliness_weights = [1, 2, 1, 3, 1]
    ins.tardiness_weights = [2, 1, 2, 1, 3]

    sol = solution.Solution(ins)
    sol.sequence = [0, 1, 2, 3, 4]

    algorithm = ConstructHeuristic(sol)
    algorithm.edd()
    algorithm.lsl()
    algorithm.osl()
    print(sol.sequence)

    # instance from file
    ins_set = data_extract.extract_data_set()
    ins0 = ins_set[0]
    sol0 = solution.Solution(ins0)
    algorithm0 = ConstructHeuristic(sol0)
    algorithm0.edd()
    sol0.fam()
    print(sol0.sequence)

