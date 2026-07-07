import argparse
import json
import logging
import os
import sys
import time

import numpy as np
import pandas as pd
import yaml
def main():

    parser = argparse.ArgumentParser(
        description="Minimal MLOps Batch Job"
    )

    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)

    args = parser.parse_args()
        logging.basicConfig(
        filename=args.log_file,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s"
    )

    start_time = time.perf_counter()

    version = "unknown"

    logging.info("Job started")

    try:         # Load config
        if not os.path.exists(args.config):
            raise FileNotFoundError("Config file not found")

        with open(args.config, "r") as file:
            config = yaml.safe_load(file)

        # Validate required keys
        required_keys = ["seed", "window", "version"]

        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing config key: {key}")

        seed = config["seed"]
        window = config["window"]
        version = config["version"]

        np.random.seed(seed)

        logging.info(
            f"Config loaded: seed={seed}, window={window}, version={version}"
        )
