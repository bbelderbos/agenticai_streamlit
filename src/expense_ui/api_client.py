import httpx


class ExpenseAPIClient:
    def __init__(self, base_url: str, timeout: float = 30.0):
        self.base_url = base_url
        self.timeout = timeout
        print(f"[API] Initialized client with base_url={base_url}")

    def _user_headers(self, user_id: int | None) -> dict:
        return {"X-User-ID": str(user_id)} if user_id is not None else {}

    def get_expenses(self, user_id: int | None = None) -> list[dict]:
        response = httpx.get(
            f"{self.base_url}/expenses/",
            headers=self._user_headers(user_id),
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json().get("items", [])

    def classify_expense(self, description: str, user_id: int | None = None) -> dict:
        response = httpx.post(
            f"{self.base_url}/expenses/classify",
            json={"description": description},
            headers=self._user_headers(user_id),
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def delete_expense(self, expense_id: int, user_id: int | None = None) -> None:
        response = httpx.delete(
            f"{self.base_url}/expenses/{expense_id}",
            headers=self._user_headers(user_id),
            timeout=self.timeout,
        )
        response.raise_for_status()

    def get_summary(self, user_id: int | None = None) -> dict:
        response = httpx.get(
            f"{self.base_url}/analytics/summary",
            headers=self._user_headers(user_id),
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()
