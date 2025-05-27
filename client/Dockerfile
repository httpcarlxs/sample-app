FROM python:3.11-alpine
WORKDIR /app
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY client.py .
CMD ["python3", "-u", "client.py"]
