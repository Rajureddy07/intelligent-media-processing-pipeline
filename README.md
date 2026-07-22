# 🚗 Intelligent Media Processing Pipeline

An AI-powered backend system that processes uploaded vehicle images asynchronously and generates structured analysis reports using OCR and image processing techniques.

The system is built with **Flask**, **PostgreSQL**, **EasyOCR**, and **OpenCV**, and follows an asynchronous processing pipeline to efficiently analyze uploaded media.

---

## Features

- Upload vehicle images via REST API
- Asynchronous background image processing
- PostgreSQL database integration
- OCR-based text extraction using EasyOCR
- Vehicle number detection and validation
- Blur detection
- Brightness analysis
- Resolution analysis
- Duplicate image detection
- Screenshot detection
- Metadata analysis
- Tamper detection
- Confidence scoring
- Retry mechanism for failed processing
- Docker support
- Logging and error handling
- Automated API testing using Pytest
---

# Tech Stack
### Backend
- Python 3.12
- Flask

### Database
- PostgreSQL
- SQLAlchemy

### Image Processing
- OpenCV
- EasyOCR
- Pillow
- imagehash

### Utilities
- NumPy
- python-dotenv
- uuid
- threading

---


# Project Structure

```
project/
│
├── app.py
├── config.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
│
├── database/
│   ├── db.py
│   └── models.py
│
├── routes/
│   ├── upload.py
│   ├── status.py
│   └── results.py
│
├── services/
│   ├── upload_service.py
│   ├── ocr/
│   └── analysis/
│
├── workers/
│   ├── processor.py
│   └── task_queue.py
│
├── tests/
│
├── uploads/
├── logs/
└── utils/
```

---

# System Architecture

```
             +----------------+
             |     Client     |
             +--------+-------+
                      |
                      |
              POST /api/upload
                      |
                      ▼
             +----------------+
             |   Flask API    |
             +--------+-------+
                      |
             Save Image & Metadata
                      |
                      ▼
             +----------------+
             | PostgreSQL DB  |
             +--------+-------+
                      |
             Push Processing ID
                      |
                      ▼
             +----------------+
             |  Task Queue    |
             +--------+-------+
                      |
                      ▼
             +----------------+
             | Background     |
             | Worker         |
             +--------+-------+
                      |
          OCR + Image Analysis Modules
                      |
                      ▼
             Save Analysis Results
                      |
                      ▼
             GET /api/results/{id}
```

---

# Processing Flow

1. User uploads an image.
2. Image is stored locally.
3. Metadata is saved in PostgreSQL.
4. A unique Processing ID is generated.
5. Processing ID is pushed into the task queue.
6. Background worker processes the image.
7. OCR extracts text.
8. Image analysis modules execute.
9. Results are stored in PostgreSQL.
10. Client retrieves processing status and final report.

---

# REST API

## 1. Upload Image

**POST**

```
/api/upload
```

Response

```json
{
  "success": true,
  "processing_id": "xxxxxxxx",
  "status": "Pending"
}
```

---

## 2. Check Processing Status

**GET**

```
/api/status/<processing_id>
```

Response

```json
{
  "processing_id": "...",
  "status": "Completed"
}
```

---

## 3. Fetch Analysis Report

**GET**

```
/api/results/<processing_id>
```

Response

```json
{
  "processing_id": "...",
  "status": "Completed",
  "analysis": {
    "...": "..."
  }
}
```

---

# AI Analysis Modules

The background worker performs the following analyses:

- OCR Text Extraction
- Vehicle Number Detection & Validation
- Blur Detection
- Brightness Analysis
- Resolution Analysis
- Duplicate Image Detection
- Screenshot Detection
- Metadata Analysis
- Tamper Detection
- Confidence Score Generation

---

# Vehicle Number Detection

Vehicle numbers are detected from OCR output using pattern matching and validation based on Indian registration formats.

If OCR confidently extracts a valid registration number, the API returns:

```json
{
  "vehicle_number": {
    "number": "MH12AB1234",
    "valid": true
  }
}
```

If no reliable registration number is detected, the API safely returns:

```json
{
  "vehicle_number": {
    "number": null,
    "valid": false
  }
}
```

This avoids false positives and ensures only validated vehicle numbers are returned.

---

# Queue Strategy

The application uses an in-memory task queue.

The Upload API immediately returns a Processing ID while image analysis is performed asynchronously by a background worker.

---

# Database

### PostgreSQL

Main table:

**Advertisements**

Stores:

- Processing ID
- Image Path
- Processing Status
- Analysis Report
- Retry Count
- Created Timestamp

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
cd intelligent-media-processing-pipeline
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=offline_ads
DB_USER=postgres
DB_PASSWORD=your_password
```

---

## Start PostgreSQL

```bash
pg_ctl start
```

---

## Run Application

```bash
python app.py
```

---

# Docker

Build and run using Docker Compose:

```bash
docker-compose up --build
```

---

# Testing

Run automated tests using Pytest:

```bash
python -m pytest -v
```

Example output:

```
==========================
3 passed in 0.99s
==========================
```

Tests include:

- Home endpoint
- Status endpoint
- Results endpoint

---

# AI Usage Disclosure

Generative AI tools (ChatGPT) were used as a development assistant to:

- Discuss software architecture
- Improve code organization
- Generate boilerplate code
- Suggest validation logic
- Improve documentation
- Review implementation ideas

All generated code was manually reviewed, integrated, modified, tested, and validated before inclusion in the final project.

---

# Design Decisions & Limitations

- Local storage is used instead of cloud storage.
- An in-memory queue is used instead of RabbitMQ or AWS SQS.
- OCR accuracy depends on image quality.
- Vehicle number detection returns `null` when OCR confidence is insufficient instead of producing unreliable results.
- Tamper detection is heuristic-based and intended as a lightweight solution.

---

# Future Improvements

- RabbitMQ / Redis Queue
- Cloud Storage (AWS S3)
- JWT Authentication
- Rate Limiting
- Kubernetes Deployment
- Prometheus & Grafana Monitoring
- Dedicated License Plate Detection Model
- Improved OCR using object detection
- GPU Acceleration
- CI/CD Pipeline

---

# 📸 Screenshots
## Application Dashboard

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/7c1f599d-7efe-49b4-a636-d66dee215d8e" />


---

## Upload Image

<img width="1920" height="1080" alt="Screenshot 2026-07-22 163147" src="https://github.com/user-attachments/assets/74adb355-ddc6-4499-baf7-d367a0f84b99" />


---

## Analysis Results

<img width="1920" height="1080" alt="Screenshot 2026-07-22 163651" src="https://github.com/user-attachments/assets/ef889a6d-720b-4f1e-a010-dc47d00bf99b" />


---

## Processing Status

<img width="1920" height="1080" alt="Screenshot 2026-07-22 163917" src="https://github.com/user-attachments/assets/5023f4bb-e3e7-4a2d-88fd-8d8be877a082" />


---

## Analysis Completed Successfully

<img width="1920" height="1080" alt="Screenshot 2026-07-22 170936" src="https://github.com/user-attachments/assets/898118d7-94d2-48f0-9213-8055a47bc49d" />


---

## PostgreSQL Database

<img width="1920" height="1080" alt="Screenshot 2026-07-22 170429" src="https://github.com/user-attachments/assets/20e95ecc-d24a-4758-81c9-a80b277db513" />


---

## PowerShell Execution

<img width="1920" height="1080" alt="Screenshot 2026-07-22 170812" src="https://github.com/user-attachments/assets/42901034-49d0-4915-970c-c3ad80e0f26a" />


---

## Terminal Output

<img width="1920" height="1080" alt="Screenshot 2026-07-22 170955" src="https://github.com/user-attachments/assets/c44a9a5e-82d8-4198-9ff5-c9b709f80a40" />






# Author

**G Rajasekhar Reddy**

BE Computer Science & Engineering (Data Science)


Vivekananda College of Engineering and Technology

