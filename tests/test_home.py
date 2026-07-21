def test_home(client):
    response = client.get("/")

    assert response.status_code == 200

    data = response.get_json()

    assert data["application"] == "Intelligent Media Processing Pipeline"
    assert data["status"] == "Running"