import pytest
import httpx

BACKEND_BASE_URL = "http://127.0.0.1:8000"

@pytest.mark.asyncio
async def test_action_anime_without_header() -> None:
    async with httpx.AsyncClient(base_url=BACKEND_BASE_URL) as client:
        response = await client.get("/action-anime")

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Field required"


@pytest.mark.asyncio
async def test_action_anime_invalid_url() -> None:
    async with httpx.AsyncClient(base_url=BACKEND_BASE_URL) as client:
        response = await client.get(
            "/action-anime",
            headers={"link": "https://myanimelist.net/anime/genre/999999999"}
        )

    assert response.status_code == 500 or response.status_code == 200  # зависит от поведения



@pytest.mark.asyncio
async def test_action_anime_success() -> None:
    async with httpx.AsyncClient(base_url=BACKEND_BASE_URL) as client:
        response = await client.get(
            "/action-anime",
            headers={"link": "https://myanimelist.net/anime/genre/1/Action"}
        )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    # Проверим наличие ключей
    required_keys = {"title", "score", "synopsis"}
    for item in data:
        assert required_keys <= item.keys()




@pytest.mark.asyncio
async def test_action_anime_empty_result() -> None:
    async with httpx.AsyncClient(base_url=BACKEND_BASE_URL) as client:
        response = await client.get(
            "/action-anime",
            headers={"link": "https://example.com"}
        )

    assert response.status_code in (200, 500)
    if response.status_code == 200:
        assert response.json() == []
