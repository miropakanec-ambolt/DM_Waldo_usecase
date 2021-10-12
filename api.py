import uvicorn
import os
import io

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from argparse import ArgumentParser

from utilities.utilities import get_uptime
from utilities.logging.config import initialize_logging, initialize_logging_middleware

from static.render import render
from starlette.responses import HTMLResponse
from fastapi import FastAPI, UploadFile, File
from PIL import Image


# --- Welcome to your Emily API! --- #
# See the README for guides on how to test it.

# Your API endpoints under http://yourdomain/api/...
# are accessible from any origin by default.
# Make sure to restrict access below to origins you
# trust before deploying your API to production.

parser = ArgumentParser()
parser.add_argument('-e', '--env', default='.env',
                    help='sets the environment file')
args = parser.parse_args()
dotenv_file = args.env
load_dotenv(dotenv_file)

app = FastAPI()

initialize_logging()
initialize_logging_middleware(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('usecase1/predict')
def predict(image: UploadFile = File(...)):
    try:
        return {
            "x": 130,
            "y": 850
        }
    except Exception as e:
        print(e)
        return { "error": f"{e}" }
    


@app.get('/health')
def test():
    return {"data": "Success"}


if __name__ == '__main__':

    uvicorn.run(
        'api:app',
        host=os.environ.get('HOST_IP'),
        port=int(os.environ.get('CONTAINER_PORT'))
    )

