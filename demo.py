from sync import Synchronized
from threading import Thread, Lock
import time

class Counter:
    def __init__(self, c=0):
        self.count = c
    @Synchronized()
    def inc(self):
        new_count = self.count+1
        #the critical section
        time.sleep(.1) #time for the counts to get out of sync
        self.count = new_count
        print "Incremented to %d."%self.count
    @Synchronized()
    def dec(self):
        new_count = self.count-1
        #the critical section
        time.sleep(.1) #time for the counts to get out of sync
        self.count = new_count
        print "Decremented to %d."%self.count
    def __repr__(self):
        return "Counter(%d)"%self.count

class DangerousThread(Thread):
    def __init__(self, counter, function, delay):
        Thread.__init__(self)
        self.counter = counter
        self.function = function
        self.delay = delay
        self.daemon = True
    def run(self):
        while True:
            self.function(self.counter)
            time.sleep(self.delay)

print "Press enter to stop."

counter = Counter()
incer = DangerousThread(counter, Counter.inc, .5)
decer = DangerousThread(counter, Counter.dec, 1)
incer.start()
decer.start()

raw_input()

print counter
print dir(counter)
