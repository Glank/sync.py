from sync import Synchronized, SynchronizationError
from threading import Thread, Lock
from types import FunctionType
import time,sys

def test_Function_Test_1():
    @Synchronized()
    def test():
        assert False, "Synchronized should have failed."
    try:
        test()
    except SynchronizationError as e:
        pass

def test_Function_Test_2():
    lock = Lock()
    @Synchronized(lock)
    def test():
        pass
    try:
        test()
    except SynchronizationError as e:
        assert False, "Non-memeber functions should still"+\
            " work with explicit locks."

def test_Class_Test():
    class Foo:
        @Synchronized()
        def test(self):
            pass
    try:
        foo = Foo()
        foo.test()
    except SynchronizationError as e:
        assert False, "Should have synced on foo."

def test_Obj_Sync_Test_1():
    stack = []
    class Counter:
        def __init__(self):
            self.count = 0
        @Synchronized()
        def inc(self):
            new = self.count+1
            time.sleep(.1)
            self.count=new
            stack.append(self.count)
    counter = Counter()
    def run():
        for i in xrange(10):
            counter.inc()
    threads = [Thread(target=run) for t in xrange(10)]
    for thread in threads:
        thread.daemon = True
        thread.start()
    for sec in range(15):
        all_stopped = True
        for thread in threads:
            if thread.isAlive():
                all_stopped = False
        if all_stopped:
            break
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(1)
    print
    for thread in threads:
        assert not thread.isAlive(), "Dead locking occured."
    last = 0
    for n in stack:
        assert n==(last+1), "Synchronization error."
        last = n

def test_Obj_Sync_Test_2():
    stack = []
    lock = Lock()
    class Counter:
        def __init__(self):
            self.count = 0
        @Synchronized(lock)
        def inc(self):
            new = self.count+1
            time.sleep(.1)
            self.count=new
            stack.append(self.count)
    counter = Counter()
    def run():
        for i in xrange(10):
            counter.inc()
    threads = [Thread(target=run) for t in xrange(10)]
    for thread in threads:
        thread.daemon = True
        thread.start()
    for sec in range(15):
        all_stopped = True
        for thread in threads:
            if thread.isAlive():
                all_stopped = False
        if all_stopped:
            break
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(1)
    print
    for thread in threads:
        assert not thread.isAlive(), "Dead locking occured."
    last = 0
    for n in stack:
        assert n==(last+1), "Synchronization error."
        last = n

def test_Func_Sync_Test():
    stack = []
    lock = Lock()
    count = [0]
    @Synchronized(lock)
    def inc():
        new = count[0]+1
        time.sleep(.1)
        count[0] = new
        stack.append(count[0])
    def run():
        for i in xrange(10):
            inc()
    threads = [Thread(target=run) for t in xrange(10)]
    for thread in threads:
        thread.daemon = True
        thread.start()
    for sec in range(15):
        all_stopped = True
        for thread in threads:
            if thread.isAlive():
                all_stopped = False
        if all_stopped:
            break
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(1)
    print
    for thread in threads:
        assert not thread.isAlive(), "Dead locking occured."
    last = 0
    for n in stack:
        assert n==(last+1), "Synchronization error."
        last = n

if __name__=="__main__":
    globes = list(globals().items())
    globes = sorted(globes, key=lambda x:x[0])
    for key, member in globes:
        if key.startswith('test_'):
            if isinstance(member, FunctionType):
                print "Starting %s..."%key[5:]
                member()
            print "%s passed."%key[5:]
    print "#"*10
    print "All tests passed."
