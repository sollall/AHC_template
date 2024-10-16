import builtins
from omegaconf import DictConfig
import importlib
import time

origin_print = print

class Test_IO:
    def __init__(self, prob_no):
        self.file_path = f"in/{str(prob_no).zfill(4)}.txt"
        self.reader = self._readline()
        self.out_path = f"out/{str(prob_no).zfill(4)}.txt"

        with open(self.out_path, "w") as f:
            pass
        return

    def _readline(self):
        with open(self.file_path) as f:
            for line in f:
                yield line.strip()

    def input(self):
        return next(self.reader)

    def output(self, *args):
        with open(self.out_path, "a") as f:
            origin_print(*args, file=f)

        return

def replace_io(prob_no):
    test_io = Test_IO(prob_no)
    builtins.input = test_io.input
    builtins.print = test_io.output

    return 

def run_module(module_name:str,params_opt:DictConfig,prob_no):
    
    module = importlib.import_module(module_name)
    if hasattr(module, "solve"):
        pass
    else:
        raise Exception(f"Module '{module_name}' does not have a 'solve' function.")
    
    start=time.time()
    
    replace_io(prob_no)
    
    score=module.solve(**params_opt)
    passed_time=time.time()-start

    return score,passed_time