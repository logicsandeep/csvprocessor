
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
        # Try multiple encodings to handle special characters in column headers
        try:
            df = pd.read_csv(temp_input_path, keep_default_na=False, na_values=[''], dtype=str, encoding='utf-8-sig')
            print("Successfully read CSV with utf-8-sig encoding")
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(temp_input_path, keep_default_na=False, na_values=[''], dtype=str, encoding='utf-8')
                print("Successfully read CSV with utf-8 encoding")
            except UnicodeDecodeError:
                try:
                    df = pd.read_csv(temp_input_path, keep_default_na=False, na_values=[''], dtype=str, encoding='latin-1')
                    print("Successfully read CSV with latin-1 encoding")
                except UnicodeDecodeError:
                    # Last resort: try with error handling
                    df = pd.read_csv(temp_input_path, keep_default_na=False, na_values=[''], dtype=str, encoding='utf-8', errors='replace')
                    print("Successfully read CSV with utf-8 encoding and error replacement")
        
        # Debug: Print column names to help identify the correct columns
        print(f"CSV columns: {list(df.columns)}")
        print(f"Total columns: {len(df.columns)}")
        for i, col in enumerate(df.columns):
            print(f"Column {i}: '{col}'")
        
        # Check for and fix "Schedule Name©" column if it's being misinterpreted
        schedule_name_found = False
        for i, col in enumerate(df.columns):
            if 'Schedule' in col and 'Name' in col:
                print(f"Found Schedule Name column at position {i}: '{col}'")
                schedule_name_found = True
                break
        
        if not schedule_name_found:
            print("WARNING: Schedule Name column not found with expected name")
            # Look for columns that might contain the schedule name data
            for i, col in enumerate(df.columns):
                if any(keyword in col.lower() for keyword in ['schedule', 'program', 'course', 'class']):
                    print(f"Potential schedule column at position {i}: '{col}'")
        
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
        
        # Create temporary Excel file for output
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xlsx', delete=False) as temp_output:
            temp_output_path = temp_output.name
        
        # Create Excel file with two tabs
        with pd.ExcelWriter(temp_output_path, engine='openpyxl') as writer:
            # Tab 1: Filtered data
            filtered_df.to_excel(writer, sheet_name='Filtered', index=False)
            
            # Tab 2: Original data (all columns including Schedule Name)
            # Include all columns from the original CSV
            original_df = df.copy()
            print(f"Including all {len(original_df.columns)} columns in Original tab")
            
            # Check if Schedule Name column exists and log its details
            schedule_columns = [col for col in original_df.columns if 'Schedule' in col and 'Name' in col]
            if schedule_columns:
                print(f"Schedule Name column(s) found: {schedule_columns}")
                for col in schedule_columns:
                    non_empty_count = original_df[col].notna().sum()
                    print(f"Column '{col}' has {non_empty_count} non-empty values out of {len(original_df)} rows")
            else:
                print("No Schedule Name column found in the data")
            
            original_df.to_excel(writer, sheet_name='Original', index=False)
        
        # Clean up input file
        os.unlink(temp_input_path)
        
        # Return the Excel file
        return FileResponse(
            path=temp_output_path,
            filename="Student_Data_Processed.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
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