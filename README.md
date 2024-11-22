# File Upload API with Django and Django REST Framework

This project provides an API for uploading and managing files using **Django** and **Django REST Framework (DRF)**.

---
## Features
- **File Upload**: Allows users to upload files with validation for size (up to 5 MB).
- **File List**: Retrieves a list of all uploaded files with metadata (e.g., file type, upload time).
- **File Retrieval**: Allows users to retrieve a specific file by its ID.
- **Filtering by File Type**: Filters files based on their type (e.g., PDF, image).
- **File Size Validation**: Prevents file uploads that exceed a 5 MB size limit.

## Prerequisites
Before running the project, make sure you have the following installed:
- Python 3.x
- Django
- Django REST Framework

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/hosametm/dj-file-upload.git
   cd dj-file-upload
   ```

2. **Create and activate a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install --upgrade pip
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Run the server**:
   ```bash
   python manage.py runserver
   ```

6. **Test the API**: Open your browser or use a tool like [Postman](https://www.postman.com/) or `curl` to interact with the API.

---

## API Endpoints

### 1. **Upload a File**
- **URL**: `/api/upload/`
- **Method**: `POST`
- **Form Data**:
  - `file` (Required): The file to upload.

- **File Size Limit**: 5 MB
- **Response**: Returns the file's ID, type, and upload timestamp.
  
Example `curl` command:
```bash
curl -X POST -F "file=@/path/to/your/file.pdf" http://127.0.0.1:8000/api/upload/
```

---

### 2. **List All Uploaded Files**
- **URL**: `/api/files/`
- **Method**: `GET`
- **Query Parameters**:
  - `file_type` (Optional): Filter files by type (e.g., `pdf`, `png`).

- **Response**: List of all uploaded files with metadata (ID, file type, and upload time).

Example `curl` command:
```bash
curl http://127.0.0.1:8000/api/files/
```

---

### 3. **Retrieve a Specific File**
- **URL**: `/api/files/{id}/`
- **Method**: `GET`
- **Path Parameter**:
  - `id` (Required): The ID of the file to retrieve.

- **Response**: Returns the file's metadata and download URL.

Example `curl` command:
```bash
curl http://127.0.0.1:8000/api/files/1/
```

---
## Technologies Used

- **Django**
- **Django REST Framework**
- **SQLite**

