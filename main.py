import io

from fastapi import FastAPI, File, HTTPException
from PIL import Image, UnidentifiedImageError
from pydantic import AnyUrl, BaseModel
from typing_extensions import Annotated

from labelled_qrcode_creator import create_label
from print_to_brother import print_label_from_image

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello"}


class LabelInfo(BaseModel):
    item_id: str
    name: str = ""
    url: AnyUrl = ""
    hcodes: list[str]
    dryrun: bool = False


@app.post("/print-label")
async def print_label_from_info(label_info: LabelInfo):
    label_image = create_label(
        url=label_info.url,
        item_id=label_info.item_id,
        name=label_info.name,
        hcodes=label_info.hcodes,
    )
    if not label_info.dryrun:
        print_label_from_image(label_image)


@app.post("/print-label-image")
async def print_label_image(file: Annotated[bytes, File()]):
    try:
        image = Image.open(io.BytesIO(file))
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid image file.")
    try:
        print_label_from_image(image)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"The following error occurred during printing: {e}"
        )
