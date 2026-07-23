import requests


API_URL = "http://127.0.0.1:8000"
http = requests.Session()
http.trust_env = False


def get_items() -> list[dict]:
    try:
        response = http.get(f"{API_URL}/items", timeout=5)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Could not GET /items: {e}") from e


def create_item(name: str, price: float, description: str | None = None) -> dict:
    try:
        response = http.post(
            f"{API_URL}/items",
            json={"name": name, "price": price, "description": description},
            timeout=5,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Could not POST /items: {e}") from e


def main() -> None:
    print("GET /items")
    print(get_items())

    print("POST /items")
    created_item = create_item("Notebook", 12.5, "Created by entrypoint.py")
    print(created_item)

    print("GET /items after POST")
    print(get_items())


if __name__ == "__main__":
    main()