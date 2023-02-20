import os, sys

from torchvision.utils import pathlib
from pydantic import BaseModel
from tools.utils import save_upload_file

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.append(os.path.abspath(os.path.join(__dir__, "..")))

from fastapi import APIRouter, HTTPException, File, Query, UploadFile
from tools.infer_lesson import get_baihoc, get_relative_lesson, get_story, query_search
from routers.utils import decode_image

router = APIRouter(
    prefix="/v1",
    tags=["models"],
    responses={404: {"description": "Not found"}},
)


@router.get("/getbaihoc")
def getbaihoc():
    return get_baihoc(None)


@router.get("/getbaihoc/{id_bai_hoc}")
def getbaihoc_byid(id_bai_hoc):
    return get_baihoc(id_bai_hoc)


@router.get("/getcauchuyen")
def getcauchuyen():
    return get_story()


@router.get("/getcauchuyen/{id_content}")
def getcauchuyen_byid(id_content):
    return get_story(id_content)


class SearchBody(BaseModel):
    keyword: str


@router.post("/search/")
def search(body: SearchBody):
    print("ahihi")
    print(body)
    return query_search(body.keyword)


@router.post("/upload")
def upload(image: UploadFile = File(...)):
    try:
        save_upload_file(image, pathlib.Path("./images/" + image.filename))
        # image = await decode_image(image)
        return get_relative_lesson("./images/" + image.filename)

    except:
        e = sys.exc_info()[1]
        raise HTTPException(status_code=500, detail=str(e))
