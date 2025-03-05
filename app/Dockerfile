FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY script.py .
COPY figures_script.py .
COPY links_script.py .
COPY tests /app/tests


