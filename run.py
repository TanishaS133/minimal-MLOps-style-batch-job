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

    try:

        # Load config
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

        # Load dataset
        if not os.path.exists(args.input):
            raise FileNotFoundError("Input CSV file not found")

        try:
            df = pd.read_csv(args.input)
        except Exception:
            raise ValueError("Invalid CSV format")

        if df.empty:
            raise ValueError("Input CSV is empty")

        if "close" not in df.columns:
            raise ValueError("Missing required column: close")

        logging.info(f"Rows loaded: {len(df)}")

        # Compute rolling mean
        logging.info("Computing rolling mean")

        df["rolling_mean"] = df["close"].rolling(window=window).mean()

        # Generate signals
        logging.info("Generating signals")

        df["signal"] = np.where(
            df["rolling_mean"].notna(),
            (df["close"] > df["rolling_mean"]).astype(int),
            np.nan
        )

        # Compute metrics
        latency_ms = int((time.perf_counter() - start_time) * 1000)

        signal_rate = round(float(df["signal"].mean(skipna=True)), 4)

        metrics = {
            "version": version,
            "rows_processed": len(df),
            "metric": "signal_rate",
            "value": signal_rate,
            "latency_ms": latency_ms,
            "seed": seed,
            "status": "success"
        }

        # Write metrics to output file
        with open(args.output, "w") as file:
            json.dump(metrics, file, indent=2)

        logging.info(f"Metrics: {metrics}")
        logging.info("Job ended with status: success")
        # Print metrics to stdout
        print(json.dumps(metrics, indent=2))

    except Exception as e:

        logging.exception("Job failed")

        error = {
            "version": version,
            "status": "error",
            "error_message": str(e)
        }

        with open(args.output, "w") as file:
            json.dump(error, file, indent=2)

        print(json.dumps(error, indent=2))

        sys.exit(1)


if __name__ == "__main__":
    main()
