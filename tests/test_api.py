from app.schemas import URLInfo


def test_shorten_url(client, url_payload, example_url, code_length):
    response = client.post("/shorten", json=url_payload)
    assert response.status_code == 201

    url_info = URLInfo.model_validate(response.json())

    assert str(url_info.full_url) == example_url
    assert len(url_info.short_code) == code_length


def test_redirect_success(client, url_payload, example_url):
    create_res = client.post("/shorten", json=url_payload)
    assert create_res.status_code == 201

    code = create_res.json()["short_code"]
    response = client.get(f"/{code}", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == example_url


def test_redirect_not_found(client):
    response = client.get("/nonexistent", follow_redirects=False)
    assert response.status_code == 404
