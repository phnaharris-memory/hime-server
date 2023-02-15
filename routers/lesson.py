import os, sys 
__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.append(os.path.abspath(os.path.join(__dir__, '..')))

from fastapi import APIRouter, HTTPException, File, UploadFile
from tools.infer_lesson import get_all_lessons, get_story_by_id, get_relative_lesson
from routers.utils import decode_image

router = APIRouter(
    prefix="/v1",
    tags = ["models"],
    responses={404: {"description": "Not found"}},
)

@router.get('/getDanhSachBaiHoc')
def retrieve():
    return get_all_lessons()


@router.get('/getDanhSachCauChuyen/{idBaiHoc}')
def retrieve(idBaiHoc):
    return get_story_by_id(idBaiHoc)

@router.post('/getRelativeLesson')
async def retrieve(image: UploadFile = File(...)):
    try:
        image = await decode_image(image)
        
        return get_relative_lesson(image)

    except:
        e = sys.exc_info()[1]
        raise HTTPException(status_code=500, detail=str(e))
