# Buguard Assets API

This repository contains the backend assessment for the Buguard internship program. It provides a robust, scalable REST API built with **FastAPI** and **PostgreSQL** to manage digital assets, track their lifecycle, define relationships between them, and securely expose operations.

## Features Implemented
- **Asset CRUD**: Create, read, update, and soft-delete assets (domains, IPs, subdomains, etc.).
- **Search, Filtering & Pagination**: Paginate results, filter by `type` and `tags`, and sort dynamically.
- **Bulk Imports & Deduplication**: Upload arrays of assets in a single request. Deduplicates existing assets by merging tags (union) and metadata, updating their last seen timestamp automatically.
- **Asset Lifecycle**: Immutable `first_seen` timestamps. Soft deletion (`status: archived`). Automatically reactivating `stale` assets upon new sightings.
- **Relationships & Graph Traversal**: Directed edge relationships between assets (e.g. Domain `resolves_to` IP). Ability to fetch 1-degree graphs.
- **Authentication**: JWT Bearer token authentication securing all write operations (`POST`, `PUT`, `PATCH`, `DELETE`) while leaving read operations (`GET`) public.
- **Standardized Error Handling**: Unified `{"error": {"code": ..., "message": ...}}` envelope for 400s, 401s, 404s, 422s, and 500s.

## Design Decisions
1. **Database Strategy**: Uses PostgreSQL with native `UUID` primary keys for security and global uniqueness.
2. **Soft Deletion**: Calling `DELETE` marks an asset's status as `archived` instead of destroying records, preserving historical sighting data.
3. **Data Integrity**: Enforces `UniqueConstraint('type', 'value')` on assets to guarantee strict deduplication. Self-referential graph edges are blocked at the application level.
4. **Pydantic Validation**: Decoupled `AssetCreate`, `AssetUpdate`, and `AssetResponse` schemas strictly define payload contracts.
5. **Security**: FastAPI's `OAuth2PasswordBearer` dependency handles JWT extraction. Passwords are theoretically handled via `passlib` (currently using dummy credentials `admin`/`admin` for the assessment scope).

## Environment Variables
The application relies on a `.env` file at the root directory. 
```ini
DATABASE_URL
SECRET_KEY
ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
```

## Setup & Running via Docker (Recommended)
Ensure you have Docker and Docker Compose installed.

1. Clone the repository and navigate to it:
   ```bash
   git clone <repository_url>
   cd Buguard-Backend-Intern-Assessment
   ```
2. Build and start the containers in detached mode:
   ```bash
   docker compose up --build -d
   ```
3. The API will be immediately available at `http://localhost:8000`. 
*(Note: SQLAlchemy automatically runs migrations and creates tables on startup).*

## API Documentation (Swagger)
FastAPI automatically generates an interactive OpenAPI documentation portal.
Once the server is running, navigate to:
**[http://localhost:8000/docs](http://localhost:8000/docs)**

From there, you can view all schemas, endpoints, and test the API directly from your browser. To test protected endpoints, use the `POST /api/v1/auth/login` endpoint to get a token and paste it into the "Authorize" button at the top right.

## Automated Testing
An exhaustive Postman collection is provided containing **37 tests and over 100 assertions**, covering every requirement.

### Running via Newman (CLI)
1. Ensure Node.js is installed on your machine.
2. Install Newman globally:
   ```bash
   npm install -g newman
   ```
3. Run the test collection:
   ```bash
   newman run test/Buguard_Assets_Postman_Collection.json
   ```

### Running via Postman UI
1. Open the Postman App.
2. Click **Import** and select the `test/Buguard_Assets_Postman_Collection.json` file.
3. Open the imported collection, click the "..." menu, and select **Run collection**.
4. The tests run sequentially and automatically handle authentication and variable passing.
