FROM python:3.11-alpine
WORKDIR /app
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY server.py .
COPY server-cert.crt server-key.key tls/
EXPOSE 5000
CMD ["python3", "server.py"]