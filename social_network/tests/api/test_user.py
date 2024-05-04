import datetime
from uuid import uuid4



async def test_get_user(dataset, client):
    print('Успешное получение пользователя по id')
    user = await dataset.user()
    assert user.id is not None, "User ID should not be None"

    resp = await client.get(f"/user/get/{user.id}")

    assert resp.status_code == 200, resp.text
    
    resp_data = resp.json()
    assert resp_data["id"] == str(user.id)
    assert resp_data["username"] == user.username

async def test_login_user(dataset, client):
    print('Успешынй логин')
    password = str(uuid4())
    user = await dataset.user(password=password)

    resp = await client.post(
        "/user/login", 
        json={"id": str(user.id), "password": password}
    )
    assert resp.status_code == 200, resp.text
    
    resp_data = resp.json()
    assert resp_data["token"]

async def test_login_user_403(dataset, client):
    print('Проверим, что логин не прошел')
    password = str(uuid4())
    user = await dataset.user(password=password)

    resp = await client.post(
        "/user/login", 
        json={"id": str(uuid4()), "password": password}
    )
    
    assert resp.status_code == 403, resp.text
    resp = await client.post(
        "/user/login", 
        json={"id": str(user.id), "password": str(uuid4())}
    )
    assert resp.status_code == 403, resp.text