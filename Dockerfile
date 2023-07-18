FROM python:3.9

COPY requirements.txt /app/requirements.txt
COPY src_app /app

WORKDIR /app

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "app.py"]