# __tests__/api/routers/master/conftest.py
import pytest
import uuid


@pytest.fixture(autouse=True)
def headers():
    return {"x-tenant-id": str(uuid.uuid4())}
