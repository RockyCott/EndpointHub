# Endpoint Hub: Semantic Search for REST APIs with FastAPI + FAISS

**Endpoint Hub** is an microservice built with FastAPI that allows you to **store**, **train**, and **semantically search** REST API endpoints. It's designed for teams managing large Postman collections who want to enhance discoverability and reuse of existing APIs through natural language queries.

Powered by [SentenceTransformers](https://www.sbert.net/) and [FAISS](https://github.com/facebookresearch/faiss), EndpointHub turns endpoint metadata into embeddings for fast and accurate similarity-based search.

---

## 🚀 Features

- 📤 Upload Postman collections, store endpoints with rich metadata and module association in MongoDB
- 🧠 Train a semantic search model with SentenceTransformers + FAISS
- 🔍 Perform natural language search to find relevant API endpoints
- 📦 Export endpoints as Postman-compatible JSON
- 🐳 Docker-ready, lightweight, and extensible

---

## 🧠 How it Works

1. **Ingest**: Postman collections are parsed into individual endpoints, enriched with metadata (like `operationId`, `keywords`, and module ID), and stored in MongoDB alongside the original Postman request structure.
2. **Train**: A FAISS index is built from vector embeddings of each endpoint's description, method, path, etc.
3. **Search**: Natural language queries are embedded and compared to the indexed endpoints to retrieve the most relevant matches.

For a deep dive into how embeddings and FAISS work together, check out [`docs/search_model_documentation.md`](docs/search_model_documentation.md)

### Data Model (MongoDB Structure)

Endpoint Hub relies on two main MongoDB collections inside the `ENDPOINTHUB` database:

#### 1. `ENDPOINTS` Collection

Each document represents a single HTTP endpoint from a Postman collection and contains both **metadata** and the original **raw Postman data**. Example structure:

```jsonc
{
    "_id": "6854bf6d02b0c358ba05543b",
    "method": "PUT",
    "moduleId": "68546d9f34a4e476f128fcdb",
    "path": "/api/path1/path2/...",
    "visibility": "private", // or "public"
    "author": "John Doe",
    "createdAt": "20XX-XX-XXT01:51:12.972Z",
    "description": "This endpoint does something important",
    "keywords": "create user update profile private data...",
    "operationId": "Endpoint Name",
    "raw": { ... }, // Full Postman-compliant collection format
    "updatedAt": "20XX-XX-XXT01:54:50.630Z"
}
```

> The `raw` field stores the original request and response structure from Postman (version 2.1.0 schema). This ensures complete fidelity when exporting endpoints back.

Fields like `keywords`, `description`, and `operationId` are used to generate semantic embeddings for search.

### 2. `MODULES` Collection

Used to associate endpoints with their respective microservice module (e.g., `core`, `admin-payroll`, `schedule`, `HR`):

```jsonc
{
    "_id": "68546d9f34a4e476f128fcdb",
    "name": "ADMON PAYROLL",
    "slug": "admonpayroll",
    "swagger": "admonpagos"
},
```

This modular design allows the system to support large-scale distributed APIs and maintain contextual grouping of endpoints.

---

## 🧪 Example Use Case

Query:
> `get all active users`

Might match endpoints like:

- `GET /users/active`
- `GET /v2/users?status=active`
- `GET /user/list/active`

---

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-org/endpoint-hub.git
cd endpoint-hub
```

### 2. Run with Docker (recommended)

```bash
docker build -t endpoint-hub .
docker run -p 8000:8000 endpoint-hub
```

> Note: Image size is around ~5-6 GB due to the inclusion of pre-trained models and dependencies.

### 3. Or run locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

> Make sure MongoDB is running and connection credentials are correctly set in your `.env` file.

---

## API Endpoints

| Method | Path                    | Description                                |
| ------ | ----------------------- | ------------------------------------------ |
| `POST` | `/add-endpoint`         | Upload a Postman collection and metadata   |
| `POST` | `/train`                | Train the semantic model and FAISS index   |
| `GET`  | `/search?q=...&top_k=5` | Search top-K most similar endpoints        |
| `GET`  | `/export-endpoint/{id}` | Export a specific endpoint as Postman JSON |

---

## 🗂️ Project Structure

```plaintext
endpoint-hub/
├── app/
│   ├── api/                 # API route handlers
│   ├── core/                # App settings and DB config
│   ├── models/              # (Optional) DB models
│   ├── schemas/             # Pydantic data models
│   ├── services/            # Search and training logic
│   ├── utils/               # Helpers for NLP and parsing
│   └── main.py              # FastAPI app entry point
├── model/                   # Trained FAISS index and embeddings
├── docs/                    # Developer documentation
├── Dockerfile               # Docker container spec
├── requirements.txt         # Python dependencies
└── README.md
```

---

## Requirements

- Python 3.10+
- MongoDB
- Docker (optional, for deployment)

---

## 🤝 Contributing

We welcome contributions! Whether it's a bug fix, new feature, or improvement to the docs, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [FAISS by Facebook AI](https://github.com/facebookresearch/faiss)
- [SentenceTransformers by UKP Lab](https://www.sbert.net/)
- [FastAPI](https://fastapi.tiangolo.com/)
