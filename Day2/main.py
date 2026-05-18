import io
import os
import zipfile
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_index():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "uploadfile.html"), "r", encoding="utf-8") as f:
        return f.read()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    
    if ext not in [".csv", ".xlsx", ".xls"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only CSV and Excel files are supported.")
    
    try:
        contents = await file.read()
        if not contents:
            raise HTTPException(status_code=400, detail="The uploaded file is empty.")
        
        output_buffer = io.BytesIO()
        output_filename = f"processed_{filename}"

        if ext == ".csv":
            contents[:4096].decode("utf-8-sig", errors="strict")
            media_type = "text/csv"
        elif ext == ".xlsx":
            with zipfile.ZipFile(io.BytesIO(contents)) as workbook:
                if "xl/workbook.xml" not in workbook.namelist():
                    raise ValueError("Invalid Excel workbook.")
            media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        else:
            media_type = "application/vnd.ms-excel"

        output_buffer.write(contents)
        output_buffer.seek(0)
        
        return StreamingResponse(
            output_buffer, 
            media_type=media_type,
            headers={
                "Content-Disposition": f"attachment; filename={output_filename}",
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
    except HTTPException:
        raise
    except (UnicodeDecodeError, zipfile.BadZipFile, ValueError):
        raise HTTPException(status_code=400, detail="Invalid or corrupted file.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
