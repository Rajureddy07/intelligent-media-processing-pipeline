def test_invalid_processing_id(client):

    response = client.get("/api/status/invalid-id")

    assert response.status_code in [200, 404]

    data = response.get_json()

    assert isinstance(data, dict)