FROM python:3.10-slim

COPY main.py .

RUN pip install fastapi httpx

EXPOSE 8000 8001 8002 8003

CMD ["python", "main.py"]
