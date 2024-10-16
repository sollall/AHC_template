import importlib
import sys
import time
from concurrent.futures import ProcessPoolExecutor
import logging
import optuna
import hydra
import mlflow
from omegaconf import DictConfig

logging.basicConfig(level=logging.INFO)

def run_module(module_name:str,params_opt:DictConfig,prob_no):
    module = importlib.import_module(module_name)
    if hasattr(module, "main"):
        pass
    else:
        raise Exception(f"Module '{module_name}' does not have a 'main' function.")

    return module.main(params_opt,prob_id=prob_no)

@hydra.main(config_path='./conf', config_name='config', version_base="1.3")
def main(cfg:DictConfig):

    if cfg.general.executor_type=="ProcessPoolExecutor":
        executor_class=ProcessPoolExecutor
    else:
        raise ValueError("Please specify the executor type.")

    total_score,total_time=0,0
    with executor_class(max_workers=cfg.general.max_workers) as executor:
        results = executor.map(run_module,
                                [cfg.general.module_name for _ in range(cfg.general.num_tests)],
                                [cfg.optimizer for _ in range(cfg.general.num_tests)],
                                [i for i in range(cfg.general.num_tests)]
                            )
        for result in results:
            score,passed_time=result
            total_score+=score
            total_time+=passed_time

    logging.info(total_score)
    return total_score

if __name__ == "__main__":
    main()