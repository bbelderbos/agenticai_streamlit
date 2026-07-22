# Expense Tracker Frontend

Streamlit UI for the Expense Tracker API.

## Run

```bash
uv run streamlit run src/expense_ui/app.py
```

## Configuration

Set `API_BASE_URL` to point to your backend:

```bash
# Local development (default)
export API_BASE_URL=http://localhost:8000/api/v1

# Production
export API_BASE_URL=https://your-api.example.com/api/v1
```
