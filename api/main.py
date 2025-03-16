from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from .utils.model_loader import predict_ui_element
from .utils.code_generator import generate_html_css
from PIL import Image
import io
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="UI2HTML Converter")

app.mount("/static", StaticFiles(directory="static"), name="static")
@app.post("/convert/")
async def convert_ui_to_html(file: UploadFile = File(...)):
    if not file.filename.endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(400, "Invalid file format. Use PNG/JPEG.")

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        element_type = predict_ui_element(image)  # Виклик моделі
        html_css = generate_html_css(element_type)
        return JSONResponse({"element": element_type, "code": html_css})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/")
async def docs():
    return {"message": "UI2HTML API. Use POST /convert with an image."}
