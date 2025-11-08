# Leva Backend - Setup Complete!

## What's Been Set Up

### 1. **Complete Backend Architecture**
```
app/
├── api/v1/          FastAPI routers (bookings, finance)
├── core/            Business logic services
├── models/          SQLAlchemy database models
├── schemas/         Pydantic validation schemas
└── db/              Database session management
```

### 2. **Database & Infrastructure**
- PostgreSQL 15 installed and running
- Database `leva` created
- All tables created:
  - `organizations` - Multi-tenant support
  - `users` - User authentication (placeholder)
  - `clients` - Shipper clients
  - `bookings` - Shipment jobs
  - `payables` - Bills to carriers (what we finance)
  - `invoices` - Bills to clients (what we collect)
  - `financing_requests` - The loan records

### 3. **API Endpoints Running**

#### Health Check
- `GET /health` - Server status

#### Bookings
- `POST /api/v1/bookings/` - Create booking + payable + invoice
- `GET /api/v1/bookings/` - List all bookings

#### Finance
- `POST /api/v1/finance/payables/{payable_id}/request_financing` - Request financing

## Access Your API

- **API Documentation (Swagger)**: http://127.0.0.1:8000/docs
- **Alternative Docs (ReDoc)**: http://127.0.0.1:8000/redoc
- **Health Check**: http://127.0.0.1:8000/health

## Test Your API

### 1. Test Health Endpoint
```bash
curl http://127.0.0.1:8000/health
```

### 2. Create a Booking
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/bookings/" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": 1,
    "carrier_name": "Maersk",
    "reference_number": "BOOK-001",
    "payable_amount": 10000.00,
    "payable_due_date": "2025-12-01",
    "invoice_amount": 10500.00,
    "invoice_due_date": "2025-12-15"
  }'
```

### 3. Request Financing
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/finance/payables/1/request_financing"
```

## Key Files

- **`app/main.py`** - FastAPI application entry point
- **`app/db/session.py`** - Database connection & session management
- **`.env`** - Environment configuration (DATABASE_URL)
- **`requirements.txt`** - Python dependencies

## Development Commands

### Start the server
```bash
source venv/bin/activate
uvicorn app.main:app --reload
```

### Access PostgreSQL
```bash
/opt/homebrew/opt/postgresql@15/bin/psql leva
```

### View database tables
```sql
\dt
```

### Stop the server
Press `Ctrl+C` in the terminal

## Database Schema

```
Organizations (1) ─┐
                   ├─> Users (*)
                   ├─> Clients (*)
                   └─> Bookings (*) ─┬─> Payables (1) ──> FinancingRequests (1)
                                     └─> Invoices (1)
```

## Next Steps

1. **Add Real Authentication**
   - Replace `auth_placeholder.py` with JWT tokens
   - Add login/register endpoints
   - Implement password hashing

2. **Add Business Logic**
   - Underwriting rules in `FinanceService`
   - Payment tracking
   - Email notifications

3. **Add More Endpoints**
   - Client management (CRUD)
   - Invoice tracking
   - Payment webhooks

4. **Testing**
   - Add pytest
   - Write unit tests for services
   - Add integration tests

5. **Production Ready**
   - Use Alembic for database migrations
   - Add logging
   - Add monitoring (Sentry, DataDog)
   - Deploy to cloud (AWS, GCP, Azure)

## Important Notes

- The current auth is a **placeholder** - it auto-creates Organization ID 1
- All data is scoped to organizations for multi-tenancy
- The "God Object" pattern creates Booking + Payable + Invoice in one transaction
- Fee is currently hardcoded at 2.5%

## Resources

- FastAPI Docs: https://fastapi.tiangolo.com
- SQLAlchemy Async: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- Pydantic: https://docs.pydantic.dev

---

**Your Leva backend is ready to go!**
