FROM python:3.10-slim
RUN mkdir /app
COPY requirements.txt /app
RUN pip install --upgrade pip
RUN pip install -r app/requirements.txt --no-cache-dir
COPY . /app
WORKDIR /app
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]





# FROM python:3.10-slim
# WORKDIR /app
# COPY backend/requirements.txt .
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt --no-cache-dir
# COPY backend/ /app
# CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]