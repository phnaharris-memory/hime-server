import os, sys
import meilisearch
from torch import less
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
    query_thing,
)

from routers.utils import decode_image
from tools.infer_lesson import ser_story, ser_baihoc
from tools.ocr_img import process_ocr

router = APIRouter(
    prefix="/v1",
    tags=["models"],
    responses={404: {"description": "Not found"}},
)

client = meilisearch.Client("http://127.0.0.1:7700", "masterKey")
index_story = client.index("story")
index_lesson = client.index("lesson")


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


@router.post("/migration")
def migration():
    query_story = "SELECT * from STORY"
    query_lesson = "SELECT * from BAI_HOC"

    _stories = query_thing(query_story)
    _lessons = query_thing(query_lesson)

    stories = []
    for story in _stories:
        story = ser_story(story)
        stories.append(story)

    lessons = []
    for lesson in _lessons:
        lesson = ser_baihoc(lesson)
        lessons.append(lesson)

    index_story.add_documents(stories)
    index_lesson.add_documents(lessons)

    return "OK"


@router.post("/ocr")
def ocr(image: UploadFile = File(...)):
    try:
        save_upload_file(image, pathlib.Path("./images/" + image.filename))
        dataToSearch = process_ocr("./images/" + image.filename)
        search_opts = {
            "attributes_to_search_on": ["shorttext", "html"],
        }
        stories = index_story.search(dataToSearch, search_opts)
        lessons = index_lesson.search(dataToSearch, search_opts)
        results = stories.hits + lessons.hits
        return results
    except:
        e = sys.exc_info()[1]
        raise HTTPException(status_code=500, detail=str(e))
