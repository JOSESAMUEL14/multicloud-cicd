FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

RUN useradd --create-home --uid 10001 appuser
USER 10001

EXPOSE 5000

CMD ["python", "app.py"]