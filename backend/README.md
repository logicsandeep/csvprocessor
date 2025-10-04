# CSV Processor - Student Data Filter

A REST API and web application for processing student data CSV files. This application extracts and filters student information including names, grades, photo release status, and parent pickup authorization.

## Features

- 📊 **CSV Processing**: Upload CSV files and get filtered output
- 🎯 **Smart Column Mapping**: Automatically handles misaligned CSV data
- 🌐 **Web Interface**: Modern, responsive web UI for file upload
- 🔄 **REST API**: Programmatic access to CSV processing
- 📱 **Mobile Friendly**: Responsive design works on all devices
- ✅ **Data Validation**: Preserves empty strings as valid values

## Quick Start

### Option 1: Using Python (Recommended)

1. **Install Python 3.8+** on your system
2. **Clone or download** this project
3. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Start the server**:
   ```bash
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
6. **Open your browser** and go to: `http://localhost:8000`

### Option 2: Using Docker (Easy Deployment)

1. **Install Docker** on your system
2. **Navigate to the project directory**
3. **Build and run**:
   ```bash
   docker build -t csv-processor .
   docker run -p 8000:8000 csv-processor
   ```
4. **Open your browser** and go to: `http://localhost:8000`

## Detailed Setup Instructions

### Prerequisites

- **Python 3.8 or higher
- **pip** (Python package installer)
- **Internet connection** (for downloading dependencies)

### Step-by-Step Installation

#### For Windows:

1. **Download Python** from [python.org](https://www.python.org/downloads/)
2. **Open Command Prompt** (cmd) or PowerShell
3. **Navigate to the project folder**:
   ```cmd
   cd path\to\your\project\backend
   ```
4. **Install dependencies**:
   ```cmd
   pip install -r requirements.txt
   ```
5. **Start the server**:
   ```cmd
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

#### For macOS:

1. **Install Python** using Homebrew:
   ```bash
   brew install python
   ```
   Or download from [python.org](https://www.python.org/downloads/)
2. **Open Terminal**
3. **Navigate to the project folder**:
   ```bash
   cd /path/to/your/project/backend
   ```
4. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```
5. **Start the server**:
   ```bash
   python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

#### For Linux (Ubuntu/Debian):

1. **Install Python and pip**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```
2. **Navigate to the project folder**:
   ```bash
   cd /path/to/your/project/backend
   ```
3. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```
4. **Start the server**:
   ```bash
   python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## Usage

### Web Interface

1. **Open your browser** and go to `http://localhost:8000`
2. **Upload a CSV file** by clicking the upload area or dragging and dropping
3. **Click "Process CSV"** to filter the data
4. **Download the filtered CSV** file

### API Usage

You can also use the API programmatically:

```bash
curl -X POST "http://localhost:8000/process-csv" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_file.csv"
```

## API Endpoints

### POST `/process-csv`
Processes a CSV file and returns a filtered version.

**Parameters:**
- `file` (form-data): CSV file to process

**Response:**
- Returns a CSV file with filtered data

### GET `/`
Serves the web interface.

## Configuration

### Changing the Port

To run on a different port, modify the startup command:

```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 3000
```

### Running in Production

For production deployment, remove the `--reload` flag:

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

## Troubleshooting

### Common Issues

1. **"python-multipart not installed"**
   ```bash
   pip install python-multipart
   ```

2. **"Address already in use"**
   - Kill existing processes: `pkill -f uvicorn`
   - Or use a different port: `--port 8001`

3. **"Module not found"**
   - Make sure you're in the correct directory
   - Install dependencies: `pip install -r requirements.txt`

4. **Permission denied**
   - On Linux/macOS: `sudo pip install -r requirements.txt`
   - Or use virtual environment

### Virtual Environment (Recommended)

To avoid conflicts with other Python projects:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## File Structure

```
backend/
├── main.py              # FastAPI application
├── convertcsv.py        # Original CSV processing script
├── index.html          # Web interface
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
└── README.md          # This file
```

## Dependencies

- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **Pandas**: Data processing
- **Python-multipart**: File upload support
- **Pydantic**: Data validation

## Support

If you encounter any issues:

1. Check that all dependencies are installed
2. Ensure Python 3.8+ is being used
3. Verify the port is not already in use
4. Check the terminal for error messages

## License

This project is open source and available under the MIT License.
