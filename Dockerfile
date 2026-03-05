FROM python:3.10-slim

WORKDIR /app

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
COPY data/ /app/data/

EXPOSE 7860

ENV FLASK_APP=app.py
ENV PORT=7860

CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app:app"]
