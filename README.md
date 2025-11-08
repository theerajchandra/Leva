# Leva

A Financial Operating System for independent freight forwarders, built with FastAPI and React.

## The Problem

Independent freight forwarders (a $2T global industry) are operationally and financially underserved. They run their business on spreadsheets and email, which is inefficient and error-prone.

Their single biggest problem, however, is **cash flow**. A small forwarder must pay an ocean carrier (e.g., Maersk) on Net 30 terms. But their end-customer (the shipper) will not pay them for Net 60 or Net 90 days. This 60-day cash flow gap is a constant burden that prevents them from taking on larger clients and stunts their growth.

## The Solution

Leva is a modern, all-in-one platform that solves this problem.

First, it provides a clean software "OS" for forwarders to manage their entire workflow: bookings, clients, payables, and invoices.

Second, because Leva is the system of record, it can see verified contracts and invoices. This allows Leva to offer **embedded trade finance**. A forwarder can click a "Finance This" button on an outstanding carrier bill. Leva pays the bill instantly, and the forwarder repays Leva when their end-customer pays them.

This closes the cash flow gap, unlocking growth. Leva is a software-first underwriting and lending platform, using workflow data as its moat.

## Tech Stack

This repository is a full-stack, multi-tenant application built with a modern, production-ready stack.

| Backend | Frontend |
|---------|----------|
| FastAPI (async) | React 18 |
| PostgreSQL | TypeScript |
| SQLAlchemy (async) | React Query |
| Alembic (Migrations) | Zustand |
| Pydantic (Validation) | Chakra UI |
| JWT Authentication | Axios |

## Key Features

* **Full-Stack Authentication:** Secure JWT-based auth with `bcrypt` hashing and `HttpOnly` cookie-less token management in a Zustand store.
* **Multi-Tenant Architecture:** All data is isolated at the database level. All API queries are filtered by the user's `organization_id` extracted from the token.
* **Production-Ready Database:** Uses Alembic for version-controlled schema migrations. No `create_all()` anti-pattern.
* **Modern Frontend State:** Uses React Query for all server-side state (caching, mutations, re-fetching) and Zustand for global client-state (auth).
* **Service-Oriented Backend:** Clean separation of concerns between API routes, business logic (Services), and database models.

## How to Run (Local Development)

### 1. Prerequisites
* Python 3.11+
* Node.js 18+
* PostgreSQL 15+

### 2. Backend Setup

```bash
# From project root: /Leva
# 1. Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Setup PostgreSQL
# (Assumes user 'postgres' and db 'leva_db' are created)
# (Update /alembic.ini and /app/db/session.py if your config is different)

# 4. Run database migrations
alembic upgrade head

# 5. Start the backend server
uvicorn app.main:app --reload
```

Backend will be running at http://127.0.0.1:8000.

### 3. Frontend Setup

```bash
# From a new terminal in the frontend folder: /Leva/frontend
# 1. Install Node modules
npm install

# 2. Start the React dev server
npm start
```

Frontend will be running at http://localhost:3000.

### 4. Test the Application

1. Navigate to http://localhost:3000/register.
2. Create a new organization and user.
3. You will be redirected to `/login`. Log in with your new credentials.
4. You will be authenticated and redirected to the main dashboard.

5. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

### Health Check
- `GET /health` - Check API status

### Bookings
- `POST /api/v1/bookings/` - Create a new booking with payable and invoice
- `GET /api/v1/bookings/` - List all bookings for organization

### Finance
- `POST /api/v1/finance/payables/{payable_id}/request_financing` - Request financing for a payable

## Core Concepts

### Multi-tenancy
All data is scoped to an `Organization`. Every request validates that the user can only access their org's data.

### God Object Pattern
Creating a booking also creates its related `Payable` (bill to carrier) and `Invoice` (bill to client) in a single transaction.

### Financial Flow
1. Freight forwarder creates a `Booking`
2. System creates `Payable` (what they owe to carrier)
3. System creates `Invoice` (what client owes them)
4. Forwarder clicks "Finance This" → creates `FinancingRequest`
5. Leva pays the carrier immediately
6. Leva collects from the client later (with 2.5% fee)

## Development

The application will automatically create database tables on startup using SQLAlchemy's `create_all()`.

For production, consider using Alembic for database migrations.

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
