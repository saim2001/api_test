import pandas as pd
from fastapi import FastAPI,File,UploadFile
from fastapi.responses import Response
from io import BytesIO,StringIO

app = FastAPI()

@app.post('/upload-excel/')
async def upload_excel(file: UploadFile = File(...)):

    contents = await file.read()
    excelData = BytesIO(contents)

    dataFrame = pd.read_excel(excelData)
    