from threading import Lock
import inspect

class SynchronizationError(RuntimeError):
    def __init__(self):
        RuntimeError.__init__(
            self,
            "Default Synchronized() call only "+
            "applicable to instance methods."
        )

class Synchronized:
    """An Object-conscious Synchronization Decorator"""
    #This static lock is so different locks do not get
    #assigned to the same object
    __locking_lock__ = Lock()
    def __init__(self, lock=None):
        """By default, the None lock implies that this
        Synchronized function is a instance method
        that will be called with an object instance as
        the first argument. A new lock will be placed on
        that object the first time a synchronized method
        is called with it."""
        self.lock = lock
    def __call__(self, f):
        self.caller = inspect.stack()[1][3]
        #get the owner of the decorated function;
        # it must be a Class to use the default
        # object lock because it will need to have
        # an object to lock.
        self.valid = False #assume invalid call
        def newFunction(*args, **kw):
            l = self.lock
            #if a lock was not specified
            if l is None:
                #and if validity has not been established
                if not self.valid:
                    if len(args)<1:
                        raise SynchronizationError()
                    caller = self.caller
                    clz = args[0].__class__
                    if caller == clz.__name__:
                        self.valid = True
                    for base in clz.__bases__:
                        if caller == base.__name__:
                            self.valid = True
                    if not self.valid:
                        raise SynchronizationError()
                #else assign a lock if the object doesn't have one
                with Synchronized.__locking_lock__:
                    if not hasattr(args[0], '__lock__'):
                        args[0].__lock__ = Lock()
                l = args[0].__lock__
            with l:
                return f(*args, **kw)
        return newFunction
    #end __call__
#end Synchronized
