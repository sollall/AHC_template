from concurrent.futures import ProcessPoolExecutor
import logging
import hydra
from omegaconf import DictConfig
import mlflow
import numpy as np

from utils.inout import run_module, get_git_commit_hash, get_git_branch

logging.basicConfig(level=logging.INFO)

@hydra.main(config_path='./conf', config_name='config', version_base="1.3")
def main(cfg:DictConfig):

    # MLflow setup
    if cfg.mlflow.enabled:
        mlflow.set_tracking_uri(cfg.mlflow.tracking_uri)
        mlflow.set_experiment(cfg.mlflow.experiment_name)
        mlflow.start_run()

        # Log parameters
        mlflow.log_params(dict(cfg.optimizer))
        mlflow.log_param("module_name", cfg.general.module_name)
        mlflow.log_param("num_tests", cfg.general.num_tests)
        mlflow.log_param("max_workers", cfg.general.max_workers)

        # Log git information as tags
        git_hash = get_git_commit_hash()
        git_branch = get_git_branch()
        if git_hash:
            mlflow.set_tag("git_commit", git_hash)
        if git_branch:
            mlflow.set_tag("git_branch", git_branch)

    if cfg.general.executor_type=="ProcessPoolExecutor":
        executor_class=ProcessPoolExecutor
    else:
        raise ValueError("Please specify the executor type.")

    total_score, total_time = 0, 0
    scores = []
    times = []

    with executor_class(max_workers=cfg.general.max_workers) as executor:
        results = executor.map(run_module,
                                [cfg.general.module_name for _ in range(cfg.general.num_tests)],
                                [cfg.optimizer for _ in range(cfg.general.num_tests)],
                                [i for i in range(cfg.general.num_tests)]
                            )
        for i, result in enumerate(results):
            score, passed_time = result
            scores.append(score)
            times.append(passed_time)
            total_score += score
            total_time += passed_time

            # Log individual test metrics to MLflow
            if cfg.mlflow.enabled:
                mlflow.log_metric(f"test_{i:04d}_score", score, step=i)
                mlflow.log_metric(f"test_{i:04d}_time", passed_time, step=i)

    # Calculate statistics
    scores_array = np.array(scores)
    times_array = np.array(times)

    avg_score = np.mean(scores_array)
    std_score = np.std(scores_array)
    min_score = np.min(scores_array)
    max_score = np.max(scores_array)
    avg_time = np.mean(times_array)

    logging.info(f"Total Score: {total_score}")
    logging.info(f"Average Score: {avg_score:.2f} ± {std_score:.2f}")
    logging.info(f"Score Range: [{min_score}, {max_score}]")
    logging.info(f"Average Time: {avg_time:.4f}s")

    # Log aggregate metrics to MLflow
    if cfg.mlflow.enabled:
        mlflow.log_metric("total_score", total_score)
        mlflow.log_metric("avg_score", avg_score)
        mlflow.log_metric("std_score", std_score)
        mlflow.log_metric("min_score", min_score)
        mlflow.log_metric("max_score", max_score)
        mlflow.log_metric("total_time", total_time)
        mlflow.log_metric("avg_time", avg_time)

        mlflow.end_run()

    return total_score

if __name__ == "__main__":
    main()