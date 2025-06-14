FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip && pip install -r /app/requirements.txt

EXPOSE 9080

COPY ./ /app

CMD ["python", "main.py"]