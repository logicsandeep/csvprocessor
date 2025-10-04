
from fastapi import FastAPI, UploadFile, Form, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pandas as pd
import os
import tempfile

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Removed OpenAI functionality to focus on CSV processing

@app.get("/health")
async def health_check():
    """Health check endpoint for Railway"""
    return {"status": "healthy", "message": "CSV Processor is running"}

@app.post("/process-csv")
async def process_csv(file: UploadFile = File(...)):
    """
    Process CSV file and return filtered CSV with Student, Grade, Photo Release, and Parent Pickup columns
    """
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be a CSV file")
        
        # Read the uploaded CSV file
        contents = await file.read()
        
        # Create temporary file for input
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.csv', delete=False) as temp_input:
            temp_input.write(contents)
            temp_input_path = temp_input.name
        
        # Process the CSV using the same logic as convertcsv.py
        df = pd.read_csv(temp_input_path, keep_default_na=False, na_values=[''], dtype=str)
        
        # The CSV data is misaligned, so we need to map to the correct columns:
        # Student names are in "Mobile Phone" column (position 6)
        # Grades are in "Gender" column (position 14) 
        # Photo Release is in "Authorized to Pickup" column (position 18)
        # Parent Pickup is in "Parent Pickup" column (position 17)
        
        # Create a new DataFrame with the correct data
        filtered_df = pd.DataFrame({
            'Student': df.iloc[:, 6],  # Mobile Phone column has student names
            'Grade': df.iloc[:, 14],   # Gender column has the actual grades
            'Photo Release': df.iloc[:, 18],  # Authorized to Pickup column has Photo Release
            'Parent Pickup': df.iloc[:, 17]  # Parent Pickup column is correct
        })
        
        # Create temporary file for output
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_output:
            filtered_df.to_csv(temp_output.name, index=False, na_rep='')
            temp_output_path = temp_output.name
        
        # Clean up input file
        os.unlink(temp_input_path)
        
        # Return the filtered CSV file
        return FileResponse(
            path=temp_output_path,
            filename="Filtered.csv",
            media_type="text/csv"
        )
        
    except Exception as e:
        # Clean up files in case of error
        if 'temp_input_path' in locals():
            try:
                os.unlink(temp_input_path)
            except:
                pass
        if 'temp_output_path' in locals():
            try:
                os.unlink(temp_output_path)
            except:
                pass
        
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serve the frontend HTML page"""
    with open("index.html", "r") as f:
        return HTMLResponse(content=f.read())