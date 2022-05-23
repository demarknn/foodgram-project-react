FROM python:3.10-slim
RUN mkdir /app
COPY backend/requirements.txt /app
RUN pip install --upgrade pip
RUN pip install -r app/requirements.txt --no-cache-dir
COPY backend/ /app
WORKDIR /app
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]
