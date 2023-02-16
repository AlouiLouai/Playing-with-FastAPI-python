FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./ /app

CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]