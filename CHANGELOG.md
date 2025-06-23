# Changelog

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) and follows the format from [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.0.0] - 2025-06-22

### 🎉 Added

- Initial public release of **Endpoint Hub**
- Core FastAPI app with semantic search endpoints:
  - `POST /add-endpoint` to upload Postman collections
  - `POST /train` to build embeddings and FAISS index
  - `GET /search` to retrieve similar endpoints using natural language
  - `GET /export-endpoint/{id}` to export as Postman JSON
- MongoDB schema with two collections:
  - `ENDPOINTS` for individual API endpoint metadata and raw Postman data
  - `MODULES` to group endpoints by microservice
- Semantic search using SentenceTransformers (`all-MiniLM-L6-v2`) + FAISS
- Preprocessing of text with custom stopword removal and intent-based query refinement
- Dockerfile and `docker-compose.yml` for containerized setup
- `.env.example` for environment variable configuration
- Developer documentation:
  - `README.md` with usage, API docs, and data model
  - `docs/search_model_documentation.md` and `fundamentos_matematicos_texto.md` as internal notes

---

## 🔜 Upcoming

- [ ] Implement `POST /add-endpoint` for uploading and parsing Postman collections
- [ ] Add a script to convert Postman collections to the required MongoDB structure
