#official Python 3.9 slim image
FROM python:3.9-slim
#working directory inside the container
WORKDIR /app
#Copy the requirements
COPY requirements.txt .
# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy the rest
COPY . .
#Default command
CMD [
    "python",
    "run.py",
    "--input", "data.csv",
    "--config", "config.yaml",
    "--output", "metrics.json",
    "--log-file", "run.log"
]
