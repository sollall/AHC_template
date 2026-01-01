import logging
from omegaconf import OmegaConf
import mlflow
import argparse

from utils.inout import run_module, parse_args, parse_unknown_args, get_git_commit_hash, get_git_branch

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    # Parse all arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--module_name', type=str, required=True)
    parser.add_argument('--test_id', type=str, required=True)
    parser.add_argument('--mlflow', action='store_true', help='Enable MLflow logging')
    parser.add_argument('--experiment_name', type=str, default='AHC_debug', help='MLflow experiment name')
    parser.add_argument('--tracking_uri', type=str, default='./mlruns', help='MLflow tracking URI')
    args, unknown = parser.parse_known_args()

    # Parse optimizer parameters
    refine_unknown = parse_unknown_args(unknown)
    cfg_opt = OmegaConf.create(refine_unknown)

    # MLflow setup for debug mode
    if args.mlflow:
        mlflow.set_tracking_uri(args.tracking_uri)

        # Generate dynamic experiment name: base_name_module_commit
        git_hash = get_git_commit_hash()
        module_name = args.module_name.replace('/', '_').replace('.', '_')

        experiment_name = args.experiment_name
        if git_hash:
            experiment_name = f"{experiment_name}_{module_name}_{git_hash[:7]}"
        else:
            experiment_name = f"{experiment_name}_{module_name}"

        mlflow.set_experiment(experiment_name)
        mlflow.start_run()

        # Log parameters
        mlflow.log_params(dict(cfg_opt))
        mlflow.log_param("module_name", args.module_name)
        mlflow.log_param("test_id", args.test_id)

        # Log git information as tags
        git_branch = get_git_branch()
        if git_hash:
            mlflow.set_tag("git_commit", git_hash)
        if git_branch:
            mlflow.set_tag("git_branch", git_branch)
        mlflow.set_tag("mode", "debug")

    score, execution_time = run_module(args.module_name, cfg_opt, args.test_id)

    logging.info(f"Test ID: {args.test_id}")
    logging.info(f"Score: {score}")
    logging.info(f"Execution Time: {execution_time:.4f}s")

    # Log metrics to MLflow
    if args.mlflow:
        mlflow.log_metric("score", score)
        mlflow.log_metric("execution_time", execution_time)
        mlflow.log_metric("test_id", int(args.test_id))

        mlflow.end_run()
