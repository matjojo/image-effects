import queue    # For Python 2.x use 'import Queue as queue'
import threading, time, random


def func(id, result_queue):
    print("Thread", id)
    slptime = random.random() * 5
    time.sleep(slptime)
    print("Thread ", id, " slept", slptime, " time" )
    result_queue.put((id, 'done', slptime))

def main():
    q = queue.Queue()
    threads = [threading.Thread(target=func, args=(0, q)), threading.Thread(target=func, args=(1,q))]
    for th in threads:
        th.daemon = True
        th.start()

    results = [0, 0]
    results[0] = q.get()
    results[1] = q.get()


    resultssorted = [0, 0]
    resultssorted[results[0][0]] = (results[0][1], results[0][2]) # we sort the results by making use of the fact that the first [0] slot in the table is the threadID, this ID we then use to determine
    resultssorted[results[1][0]] = (results[1][1], results[1][2]) # the spot it gets in the sorted table, thus making sure that the first [0] slot in that table is the one from the first [0] thread

    print(resultssorted)


if __name__=='__main__':
    main()