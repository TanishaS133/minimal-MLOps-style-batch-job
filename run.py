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
