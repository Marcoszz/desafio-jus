headers = {
    'Content-type':'application/json', 
    'Accept':'application/json'
}

url = '/processo/'

def test_api_app_is_created(app):
    assert app is not None

def test_api_invalid_court(client):
    data = {
        'process': '0710802-55.2018.8.04.0001'
    }

    response = client.post(
        url,
        json=data,
        headers=headers
    )

    assert response.status_code == 400

def test_api_invalid_segment(client):
    data = {
        'process': '0710802-55.2018.6.02.0001'
    }

    response = client.post(
        url,
        json=data,
        headers=headers
    )

    assert response.status_code == 400

def test_api_incorrect_format(client):
    data = {
        'process': '010802-55.2018.8.02.0001'
    }

    response = client.post(
        url,
        json=data,
        headers=headers
    )

    assert response.status_code == 400

def test_api_process_not_found(client):
    data = {
        'process': '0610802-55.2018.8.02.0001'
    }

    response = client.post(
        url,
        json=data,
        headers=headers
    )

    assert response.status_code == 404

def test_api_process_found(client):
    data = {
        'process': '0710802-55.2018.8.02.0001'
    }

    response = client.post(
        url,
        json=data,
        headers=headers
    )

    assert response.status_code == 200