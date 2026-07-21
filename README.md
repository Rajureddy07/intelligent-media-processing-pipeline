# Intelligent Media Processing Pipeline

An AI-powered backend system that accepts vehicle image uploads, processes them asynchronously, and generates structured analysis reports.

---

# Features

- Upload vehicle images through REST API
- Asynchronous image processing
- PostgreSQL database integration
- OCR text extraction
- Vehicle number detection & validation
- Blur detection
- Brightness analysis
- Resolution analysis
- Duplicate image detection
- Screenshot detection
- Metadata analysis
- Tamper detection
- Confidence scoring
- Retry mechanism
- Docker support
- Logging

---

# Tech Stack

Backend
- Python 3.12
- Flask

Database
- PostgreSQL
- SQLAlchemy

Image Processing
- OpenCV
- EasyOCR
- Pillow
- imagehash

Utilities
- python-dotenv
- NumPy

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
│   └── analysis/
│
├── workers/
│   ├── processor.py
│   └── task_queue.py
│
├── uploads/
├── logs/
├── utils/
└── README.md
```

---

# Architecture

```
Client
   │
   ▼
Upload API
   │
   ▼
Store Image
   │
   ▼
Save Metadata
   │
   ▼
Task Queue
   │
   ▼
Background Worker
   │
   ▼
Image Analysis
   │
   ▼
Store Results
   │
   ▼
Results API
```

---

# Processing Flow

1. User uploads an image.
2. Image is stored locally.
3. Metadata is stored in PostgreSQL.
4. A unique Processing ID is generated.
5. The Processing ID is pushed to the task queue.
6. Background worker processes the image.
7. AI analysis modules generate results.
8. Results are stored in PostgreSQL.
9. User fetches processing status.
10. User retrieves analysis report.

---

# APIs

## Upload Image

POST

```
/api/upload
```

Response

```json
{
  "success": true,
  "processing_id": "...",
  "status": "Pending"
}
```

---

## Processing Status

GET

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

## Analysis Result

GET

```
/api/results/<processing_id>
```

Response

```json
{
  "processing_id":"...",
  "status":"Completed",
  "analysis":{...}
}
```

---

# AI Modules

- OCR Extraction
- Vehicle Number Validation
- Blur Detection
- Brightness Detection
- Resolution Analysis
- Duplicate Detection
- Screenshot Detection
- Metadata Analysis
- Tamper Detection
- Confidence Scoring

---

# Queue Strategy

An in-memory queue is used for asynchronous processing.

The Upload API immediately returns a Processing ID while the background worker processes the image independently.

---

# Database

PostgreSQL

Main table:

Advertisements

Stores

- Processing ID
- Image path
- Status
- Analysis result
- Retry count

---

# Running Locally

## Install dependencies

```
pip install -r requirements.txt
```

## Configure environment

Create `.env`

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=offline_ads
DB_USER=postgres
DB_PASSWORD=your_password
```

## Start PostgreSQL

```
pg_ctl start
```

## Run application

```
python app.py
```

---

# Docker

```
docker-compose up --build
```

---

# AI Usage Disclosure

AI tools such as ChatGPT were used to:

- Discuss architecture decisions
- Improve code structure
- Generate boilerplate
- Suggest validation logic
- Improve error handling
- Help design retry mechanism
- Improve documentation

All generated code was manually reviewed, integrated, tested, and modified to fit the project requirements.

---

# Trade-offs

To keep the project simple:

- Local storage was used instead of cloud storage.
- An in-memory queue was used instead of RabbitMQ/SQS.
- Simple heuristic-based tamper detection was implemented.
- OCR accuracy depends on image quality.

---

# Future Improvements

- RabbitMQ
- Redis Queue
- Kubernetes deployment
- Cloud storage
- JWT Authentication
- Rate limiting
- Prometheus monitoring
- ML-based tamper detection
- GPU inference
- CI/CD pipeline

---

# Author

Rajasekhar Reddy