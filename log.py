from multiprocessing import Process, Queue
from datetime import datetime
import time
import sys
import os

class Logger():
    def __init__(self):
        # profiling
        self.profiles = {}
        
        # loglevels
        self.DEBUG = 0
        self.DEFAULT = 1
        self.INFO = 2

    def init(self, file_path, log_level=0, verbose=False, use_subprocess=True, date_in_name=True, folder_path=""):
        # settings
        self.verbose = verbose
        self.use_subprocess = use_subprocess
        self.log_level = log_level
        #TODO: add a var for profiling in general
        #TODO: add splitting to folders instead of folder_path

        # pre init logs
        self.pre_q = []

        # file
        if not folder_path.endswith("/") or not folder_path.endswith("\\"):
            folder_path += "/"
            if not os.path.exists(folder_path):
                self.pre_q.append(f"[INFO] the folder '{folder_path}' does not exist. It will be created")
                os.mkdir(folder_path)

        if '.txt' in file_path:
            if date_in_name:
                self.file_path = f"{file_path.split('.txt')[0]}_{datetime.now().strftime('%d%m%Y_%H%M%S')}.txt"
            else:
                self.file_path = folder_path + file_path   
        else:
            self.pre_q.append(f"[INFO] file_path {file_path} not correct. Must be a .txt file")
            self.file_path = f"log_{datetime.now().strftime('%d%m%Y_%H%M%S')}.txt"
            self.pre_q.append(f"[INFO] use '{self.file_path}' as file name")
        self.pre_q.append(f"[INFO] log_level is set to {self.get_loglevel_name()}:{self.log_level}")
        self.file_path = folder_path + self.file_path    

        # start handlers
        # subprocess
        if self.use_subprocess:
            self.queue = Queue()
            self.p = Process(target=self.subproc_save, args=(self.queue, self.file_path,))
            self.p.start()
            self.print_info(f"start subprocess and write to file '{self.file_path}'", verbose=False)
        # one process for everything
        else:
            self.f = open(self.file_path, "a")
            self.log(f"write to file '{self.file_path}' without a subprocess")

        # write pre init logs to the log file
        for item in self.pre_q:
            self.log(item, log.INFO)
        del self.pre_q

    def print_error(self, input_string, verbose=True, quit=False):
        self.log(f"[ERROR] {input_string}", verbose=verbose)
        if quit:
            sys.exit()
            
    def print_info(self, input_string, verbose=True):
        self.log(f"[INFO] {input_string}", verbose=verbose)

    # function wrappers
    def debug(self, func):
        #TODO: add more information
        def ret(*args, **kwargs):
            ret_string = ""
            if func.__name__ == "__init__":
                ret_string += f"[new instance]: {args[0]}"
                #ret_string += f" create: {(func.__qualname__).strip('.__init__')}"
            else:
                ret_string += f"[func call]: {func}"
            # add args unparsed
            ret_string += f"{args}"
            self.log(ret_string, lvl=self.DEBUG)
            
            # call function
            try:
                ret = func(*args, **kwargs)
                return ret
            except Exception as error:
                self.print_error(error)
                return ret
        return ret
    
    def default(self, func):
        def ret(*args, **kwargs):
            ret_string = ""
            if func.__name__ == "__init__":
                ret_string += f"[new instance]: {args[0]}"
            else:
                ret_string += f"[func call]: {func.__name__}"
            
            # add args parsed
            arg_string = " "
            for arg in args:
                if arg == args[0] and not func.__name__ == "__init__":
                    arg_string += f"{str(arg)}, "
            ret_string += f"({arg_string.strip(', ')})"
            self.log(ret_string, lvl=self.DEFAULT)
            
            # call function
            try:
                ret = func(*args, **kwargs)
                return ret
            except Exception as error:
                self.print_error(error)
                return ret
        return ret
    
    def info(self, func):
        def ret(*args, **kwargs):
            ret_string = ""
            if func.__name__ == "__init__":
                ret_string += f"[new instance]: {(func.__qualname__).strip('.__init__')}"
            else:
                ret_string += f"[func call]: {func.__name__}"
            self.log(ret_string, lvl=self.INFO)
            
            # call function
            try:
                ret = func(*args, **kwargs)
                return ret
            except Exception as error:
                self.print_error(error)
                return ret
        return ret
    
    # log some string manually
    def log(self, input, lvl=-1, verbose=False):
        if self.log_level <= lvl or lvl == -1:
            ret_string = f"[{datetime.now().time()}][{self.get_loglevel_name(lvl)}] {input}"
            if self.verbose or verbose:
                print(ret_string)
            if self.use_subprocess:
                self.queue.put(ret_string)
            else:
                self.f.write(ret_string + '\n')
        
    # subprocess stuff
    def subproc_save(self, queue, file):
        f = open(file, "a")
        running = True
        while running:
            element = queue.get()
            if element == "[STOP LOGGING]":
                running = False
                f.close()
            else:
                f.write(element + '\n')
    
    def close(self):
        if self.use_subprocess:
            self.queue.put("[STOP LOGGING]")
        else:
            self.f.close()
    
    def get_loglevel_name(self, lvl=-1):
        if lvl == -1:
            lvl = self.log_level
        
        if lvl == self.DEBUG:
            return "DEBUG"
        elif lvl == self.DEFAULT:
            return "DEFAULT"
        elif lvl == self.INFO:
            return "INFO"
        return
    
    # profiling
    def profile(self, func):
        def ret(*args, **kwargs):
            start_time = time.time()
            ret = self.debug(func(*args, **kwargs))
            delta = time.time() - start_time
            func_name = func.__name__
            if not func_name in self.profiles:
                self.profiles[func_name] = {'called':0,'time':0, 'avg':0}
            self.profiles[func_name]['called'] += 1
            self.profiles[func_name]['time'] += delta
        return ret

    def print_profiling(self):
        for key in self.profiles.keys():
            self.profiles[key]['avg'] += self.profiles[key]['time'] / self.profiles[key]['called']
        #TODO: sort by time
        #self.profiles = dict(sorted(self.profiles.items(), key=lambda item: item['time']))
        #print(self.profiles.items(), key=lambda item: item['time'])
        if not self.profiles == {}:
            print(self.profiles)
        else:
            self.log("[PROFILING] no data collected")


log = Logger()


# example usage
if __name__ == "__main__":
    log.init("log.txt", folder_path="logs")
    # Dummy class for testing
    class SomeDummyClass(object):
        @log.info
        def __init__(self):
            self.some_objects = []
            for i in range(10):
                self.some_objects.append(SomeDummySubClass())
            
        def __repr__(self):
            return f"<{type(self).__name__} object at {hex(id(self))}>"
        
        def __str__(self):
            return f"<{type(self).__name__} object at {hex(id(self))}>"
        
    class SomeDummySubClass(object):
        def __init__(self):
            self.name = "name"

    # dummy function for testing
    @log.debug
    def test(test):
        #print("func:", test)
        pass

    for i in range(10):
        test(SomeDummyClass())
    
    log.print_error("an error occured")
    log.print_info("some info message")
    
    log.print_profiling()
    log.close()