import os, sys

from torchvision.utils import pathlib
from pydantic import BaseModel
from tools.utils import save_upload_file

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.append(os.path.abspath(os.path.join(__dir__, "..")))

from fastapi import APIRouter, HTTPException, File, Query, UploadFile
from tools.infer_lesson import (
    get_baihoc,
    get_relative_lesson,
    get_story,
    get_story_by_image,
    query_search,
    get_story_by_image,
)

from routers.utils import decode_image


# Update
from tools.ocr_img import tesseract_process
from meilisearch import Client
# End

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
        img_id = get_relative_lesson("./images/" + image.filename)
        print("img neeee")
        print(img_id)
        return get_story_by_image(img_id)
        # return get_relative_lesson("./images/" + image.filename)

    except:
        e = sys.exc_info()[1]
        raise HTTPException(status_code=500, detail=str(e))

# Update
search_client = Client("http://127.0.0.1:7700", "Z4bpTsc3yeTipItK22QzDGcUjjlzWOfjGQYcOmSmSEE")

@router.post("/uploadAndOcr")
def imgToText(image: UploadFile = File(...)):
    try:
        save_upload_file(image, pathlib.Path("./images/" + image.filename))
        dataToSearch = tesseract_process("./images/" + image.filename)
        results = []
        index = search_client.get_index("indexBaiHoc")
        search_result = index.search(dataToSearch)
        results.append(search_result)
        index = search_client.get_index("indexCauChuyen")
        search_result = index.search(dataToSearch)
        results.append(search_result)
        return results

    except:
        e = sys.exc_info()[1]
        raise HTTPException(status_code=500, detail=str(e))