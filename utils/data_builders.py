import uuid


def generate_unique_cat_name(prefix: str = "TestCat") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def build_cat_payload(name: str | None = None, age: int = 1, breed: str = "Test") -> dict:
    return {
        "name": name or generate_unique_cat_name(),
        "age": age,
        "breed": breed,
    }