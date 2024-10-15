import importlib
import sys
import time
from concurrent.futures import ProcessPoolExecutor
import logging
import optuna
import hydra
import mlflow

logging.basicConfig(level=logging.INFO)

def run_module(module,prob_no):
    return module.main(prob_no)

@hydra.main(config_path='./conf', config_name='config', version_base="1.3")
def main(cfg):

    module = importlib.import_module(cfg.general.module_name)
    if hasattr(module, "main"):
        pass
    else:
        raise Exception(f"Module '{cfg.general.module_name}' does not have a 'main' function.")

    if cfg.general.executor_type=="ProcessPoolExecutor":
        executor_class=ProcessPoolExecutor
    else:
        raise ValueError("Please specify the executor type.")
    with executor_class(max_workers=cfg.general.max_workers) as executor:
        results = executor.map(run_module,
                                [module for _ in range(cfg.general.num_tests)],
                                [i for i in range(cfg.general.num_tests)]
                            )

    total_score,total_time=0,0
    
    return total_score

if __name__ == "__main__":
    main()