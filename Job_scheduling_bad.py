"""BAD CODE"""

class Job:
     def __init__(self, s, f, p):
         self.s = s
         self.f = f
         self.p = p

def sched(j):
     def bs(j, s):
         l = 0
         r = s - 1

         while l <= r:
             m = (l + r) // 2
             if j[m].f <= j[s].s:
                 if j[m + 1].f <= j[s].s:
                     l = m + 1
                 else:
                     return m
             else:
                 r = m - 1
         return -1

     j.sort(key=lambda x: x.f)
     n = len(j)
     t = [0] * n
     t[0] = j[0].p

     for i in range(1, n):
         ip = j[i].p
         pos = bs(j, i)
         if pos != -1:
             ip += t[pos]
         t[i] = max(ip, t[i - 1])

     return t[n - 1]


def main():
     j = [
         Job(1, 3, 5),
         Job(2, 5, 6),
         Job(4, 6, 5),
         Job(6, 7, 4),
         Job(5, 8, 11),
         Job(7, 9, 2)
     ]
     print("Maximum profits:", sched(j))

if __name__ == "__main__":
     main()
