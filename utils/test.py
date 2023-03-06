import threading
from time import sleep


def temp(one, two, sleep_n):
    for i in range(two):
        print(one)
        sleep(sleep_n)


def temp1(one, two, sleep_n):
    for i in range(two):
        print(one)
        sleep(sleep_n)


# t1 = temp(10, 10, .1)
t = threading.Thread(target=temp, args=(10, 10, .2))
# t.daemon = True
t.start()

t1 = threading.Thread(target=temp1, args=(22, 22, .2))
# t1.daemon = True
t1.start()

t1.join()
t.join()


