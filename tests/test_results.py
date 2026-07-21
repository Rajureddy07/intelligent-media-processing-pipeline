def test_invalid_result(client):

    response = client.get("/api/results/invalid-id")

    assert response.status_code in [200, 404]

    data = response.get_json()

    assert isinstance(data, dict)