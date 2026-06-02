from app.schemas.user_schemas import UserCreate
from app.core.security import hash_password

def test_register_user(client):
    response = client.post("/users/register", json={
        "username": "teste",
        "email": "teste@teste.com",
        "password": "123456",
        "role": "employee"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "teste"

def test_create_ticket(client):
    # Cria categoria
    cat_resp = client.post("/categories/", json={"name": "TI", "description": "Suporte"})
    cat_id = cat_resp.json()["id"]
    # Cria usuário
    client.post("/users/register", json={"username": "joao", "email": "joao@e.com", "password": "123", "role": "employee"})
    # Login
    login_resp = client.post("/users/login", data={"username": "joao", "password": "123"})
    token = login_resp.json()["access_token"]
    # Criar ticket
    resp = client.post("/tickets/", json={
        "title": "Problema",
        "description": "Falha",
        "category_id": cat_id,
        "priority": "alta",
        "status": "aberto"
    }, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 201
    assert resp.json()["title"] == "Problema"