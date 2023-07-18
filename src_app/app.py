from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse
import uvicorn
import argparse
import shutil
import os

from d_ocr import donation_ocr


app = FastAPI()


@app.get("/health")
def health():
    return {"status": "OK"}


@app.get("/")
def main():
    html_content = """
            <body>
            <form action="/ocr" enctype="multipart/form-data" method="post">
            <input name="file" type="file">
            <input type="submit">
            </form>
            </body>
            """
    return HTMLResponse(content=html_content)


@app.post("/ocr")
async def process_request(file: UploadFile):
    with open("temp.png", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # send the image to the process function
    ocr = donation_ocr()
    res = ocr.predict("temp.png")
    return res


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=8000, type=int, dest="port")
    parser.add_argument("--host", default="0.0.0.0", type=str, dest="host")
    args = vars(parser.parse_args())
    uvicorn.run(app, **args)