import importlib
import sys
import time
from concurrent.futures import ProcessPoolExecutor
import logging
import optuna

logging.basicConfig(level=logging.INFO)

def run_module(module,params,prob_no):
    return module.main(prob_no,params)


def objective(experiment):
    # module_name kara module to param wo syutokusuru
    module = importlib.import_module(module_name)
    if hasattr(module, "main"):
        pass
    else:
        raise Exception(f"Module '{module_name}' does not have a 'main' function.")

    params = module.gen_params_for_optuna(experiment)

    with executor_class(max_workers=MAX_WORKERS) as executor:
        results = executor.map(run_module,
                                [module for _ in range(NUM_TESTS)],
                                [params for _ in range(NUM_TESTS)],
                                [i for i in range(NUM_TESTS)]
                            )

    total_score,total_time=0,0
    """
    for result in results:
        score,passed_time=result
        total_score+=score
        total_time+=passed_time
    """

    return total_score

if __name__ == "__main__":
    NUM_TESTS=4
    MAX_WORKERS=4

    executor_class = ProcessPoolExecutor 

    if len(sys.argv) > 1:
        module_name = sys.argv[1]
        start = time.time()

        study=optuna.create_study(direction="maximize")
        study.optimize(objective,n_trials=100)
            
        end=time.time()
        logging.info(f"Total time: {end-start:.3f} sec")
    else:
        raise Exception("Please provide a module name as an argument.")