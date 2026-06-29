# Analytics Engine v2 🚀

A production-grade FastAPI analytics microservice with **Pydantic v2** request validation and structured nested JSON responses.

---

## 📌 Assignment

**Enforcing Request Schemas and Structured JSON Validation with Pydantic**  
MCA — Project Based Learning (PBL) | BMSIT

---

## 🗂️ Project Structure

```
analytics_engine_v2/
├── .gitignore               # Excludes .venv and cache files
├── pyproject.toml           # Managed via uv
└── app/
    ├── __init__.py
    ├── main.py              # Root server entrypoint
    ├── schemas/
    │   ├── __init__.py
    │   └── data_models.py   # Pydantic request/response validation schemas
    └── routers/
        ├── __init__.py
        └── metrics.py       # Refactored router with POST endpoints
```

---

## ⚙️ Tech Stack

| Tool | Purpose |
|---|---|
| **FastAPI** | Web framework |
| **Pydantic v2** | Request/response validation |
| **Uvicorn** | ASGI server |
| **uv** | Package manager |

---

## 🧩 Pydantic Schemas

### `TransactionRequest` — Request Payload Contract

| Field | Type | Constraint |
|---|---|---|
| `unit_price` | `float` | Must be `> 0.0` |
| `quantity` | `int` | Must be `> 0` |
| `currency` | `str` | Max 3 characters, auto-uppercased |

### `AnalyticsResponse` — Nested Response Matrix

| Field | Type | Description |
|---|---|---|
| `raw_total` | `float` | `unit_price × quantity` |
| `is_bulk_order` | `bool` | `True` if `quantity >= 10` |
| `formatted_metadata` | `FormattedMetadata` | Nested object with currency + display string |

---

## 🛣️ API Endpoints

### `POST /metrics/calculate`

**Request Body:**
```json
{
  "unit_price": 45.0,
  "quantity": 10,
  "currency": "INR"
}
```

**Response `200 OK`:**
```json
{
  "raw_total": 450.0,
  "is_bulk_order": true,
  "formatted_metadata": {
    "currency": "INR",
    "display": "Total amount is ₹450.00"
  }
}
```

**Response `422 Unprocessable Entity`** (on invalid input):
```json
{
  "detail": [
    {
      "type": "greater_than",
      "loc": ["body", "unit_price"],
      "msg": "Input should be greater than 0",
      "input": -5.0
    }
  ]
}
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Hacker004rahul/analytics_engine_v2.git
cd analytics_engine_v2
```

### 2. Install dependencies
```bash
pip install fastapi uvicorn pydantic
```

### 3. Run the server
```bash
uvicorn app.main:app --reload
```

### 4. Open Swagger UI
```
http://127.0.0.1:8000/docs
```

---

## ✅ Validation Test Cases

| Test | Input | Expected |
|---|---|---|
| Valid bulk order | `qty=10, price=45, currency="INR"` | `200 OK`, `is_bulk_order: true` |
| Valid non-bulk | `qty=3, price=9.99, currency="USD"` | `200 OK`, `is_bulk_order: false` |
| Negative price | `unit_price=-5.0` | `422` → Input should be greater than 0 |
| String quantity | `quantity="abc"` | `422` → Unable to parse string as integer |
| Currency too long | `currency="EURO"` | `422` → String too long |
| Auto-uppercase | `currency="inr"` | Auto-converted to `"INR"` ✅ |

---

## 👨‍💻 Author

**Rahul** — MCA Student, BMSIT  
BMS Institute of Technology and Management, Bengaluru
