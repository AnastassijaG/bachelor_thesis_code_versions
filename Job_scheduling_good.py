""""GOOD CODE"""
class Job:
    def __init__(self, start, finish, profit):
        self.start = start
        self.finish = finish
        self.profit = profit

class Scheduler:
    def __init__(self):
        self.jobs = []

    def add_job(self, start, finish, profit):
        self.jobs.append(Job(start, finish, profit))

    def do_binary_search(self, start_index):
        left = 0
        right = start_index - 1

        while left <= right:
            mid = (left + right) // 2
            if self.jobs[mid].finish <= self.jobs[start_index].start:
                if self.jobs[mid + 1].finish <= self.jobs[start_index].start:
                    left = mid + 1
                else:
                    return mid
            else:
                right = mid - 1
        return -1

    def schedule(self):
        self.jobs.sort(key=lambda j: j.finish)
        length = len(self.jobs)
        table = [0] * length
        table[0] = self.jobs[0].profit

        for i in range(1, length):
            incl_prof = self.jobs[i].profit
            pos = self.do_binary_search(i)
            if pos != -1:
                incl_prof += table[pos]
            table[i] = max(incl_prof, table[i - 1])

        return table[length - 1]

def main():
    scheduler = Scheduler()
    scheduler.add_job(1, 3, 5)
    scheduler.add_job(2, 5, 6)
    scheduler.add_job(4, 6, 5)
    scheduler.add_job(6, 7, 4)
    scheduler.add_job(5, 8, 11)
    scheduler.add_job(7, 9, 2)
    print("Maximum profit:", scheduler.schedule())

if __name__ == "__main__":
    main()
