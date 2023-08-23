FROM python:3.9

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY app /app
COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "app.py", "run_worker.sh"]