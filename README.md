# minimal-MLOps-style-batch-job
## Overview
This project implements a minimal MLOps-style batch processing pipeline in Python.
The program:

- Loads configuration from a YAML file
- Reads OHLCV data from a CSV file
- Computes a rolling mean on the `close` column
- Generates binary trading signals
- Writes metrics to a JSON file
- Logs execution details to a log file
## Project Structure

```text
.
├── run.py
├── config.yaml
├── data.csv
├── requirements.txt
├── Dockerfile
├── README.md
├── metrics.json
└── run.log
```
## Requirements

- Python 3.9+
- pip
- Docker (optional)

---
## Install Dependencies

```bash
pip install -r requirements.txt
```

---
## Local Run
```bash
python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log
```
---
## Docker
### Build

```bash
docker build -t mlops-task .
```
### Run
```bash
docker run --rm mlops-task
```
---
## Output
The application generates:
- `metrics.json`
- `run.log`
It also prints the metrics JSON to the terminal.
---
## Example metrics.json

```json
{
  "version": "v1",
  "rows_processed": 10000,
  "metric": "signal_rate",
  "value": 0.4990,
  "latency_ms": 127,
  "seed": 42,
  "status": "success"
}
```
---
## Logging

The log file records:

- Job start
- Configuration loading
- Dataset loading
- Rolling mean computation
- Signal generation
- Metrics summary
- Job completion
