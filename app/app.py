import os
import uuid
import argparse

from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse
import uvicorn

from fastapi.responses import JSONResponse
from celery.result import AsyncResult

from tasks import process_image

from PIL import Image
import numpy as np


app = FastAPI()


@app.post("/ocr/upload", status_code=202)
async def process(file: UploadFile):
    # загрузить картинку
    img_id = str(uuid.uuid4())
    img = Image.open(file.file)
    img.save(f"./storage/{img_id}.png")
    task_id = process_image.apply_async(args=[img_id])
    return {'task_id': str(task_id), 'status': 'Processing'}


@app.get("/ocr/result/{task_id}", status_code=200,
         responses={202: {'description': 'Accepted: Not Ready'}})
async def get_status(task_id):
    task_result = AsyncResult(task_id)
    if not task_result.ready():
        return JSONResponse(status_code=202, content={'task_id': str(task_id), 'status': 'Processing'})
    result, img_id = task_result.get()
    os.remove(f"./storage/{img_id}.png")
    return {'task_id': task_id, 'status': 'Success', 'Result': result}


@app.get("/health")
def health():
    return {"status": "OK"}


@app.get("/")
def main():
    html_content = """
            <body>
            <form action="/upload" enctype="multipart/form-data" method="post">
            <input name="file" type="file">
            <input type="submit">
            </form>
            </body>
            """
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=8000, type=int, dest="port")
    parser.add_argument("--host", default="0.0.0.0", type=str, dest="host")
    args = vars(parser.parse_args())
    uvicorn.run(app, **args)