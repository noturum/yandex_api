FROM python:3.11-slim
LABEL authors="nik"
WORKDIR /app
ENV PYTHONPATH = /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python3","app.py"]