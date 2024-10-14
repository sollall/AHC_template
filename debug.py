import importlib
import sys
import time
from concurrent.futures import ProcessPoolExecutor
import logging

logging.basicConfig(level=logging.INFO)

def run_dynamic_import(module_name,prob_no):
    try:
        # モジュールを動的にインポート
        module = importlib.import_module(module_name)
        # インポートされたモジュールからmain関数を呼び出し
        if hasattr(module, "main"):
            return module.main(prob_no)
        else:
            raise Exception(f"Module '{module_name}' does not have a 'main' function.")
    except ModuleNotFoundError:
        raise Exception(f"Module '{module_name}' not found.")

if __name__ == "__main__":
    NUM_TESTS=4
    MAX_WORKERS=4

    executor_class = ProcessPoolExecutor 

    if len(sys.argv) > 1:
        module_name = sys.argv[1]
        start = time.time()
        with executor_class(max_workers=MAX_WORKERS) as executor:
            
            for i in range(NUM_TESTS):
                future = executor.map(run_dynamic_import,
                                      [module_name for _ in range(NUM_TESTS)],
                                      [i for i in range(NUM_TESTS)])
            
        end=time.time()
        logging.info(f"Total time: {end-start:.3f} sec")
        for res in future:
            logging.info(f"result: {res}")
    else:
        raise Exception("Please provide a module name as an argument.")