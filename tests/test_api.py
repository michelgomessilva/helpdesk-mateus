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


# ========== TESTES DE ERRO (AUTENTICAÇÃO E AUTORIZAÇÃO) ==========

def test_login_wrong_password(client):
    # Registra um usuário
    client.post("/users/register", json={
        "username": "joaoerro",
        "email": "joaoerro@email.com",
        "password": "123456",
        "role": "employee"
    })
    # Tenta login com senha errada
    resp = client.post("/users/login", data={"username": "joaoerro", "password": "errada"})
    assert resp.status_code == 401
    assert "Usuário ou senha incorretos" in resp.json()["detail"]

def test_create_ticket_without_token(client):
    # Primeiro cria uma categoria (pode ser sem token, se o endpoint não exigir)
    cat_resp = client.post("/categories/", json={"name": "TI", "description": "Suporte"})
    cat_id = cat_resp.json()["id"]
    # Tenta criar ticket sem token (sem cabeçalho Authorization)
    resp = client.post("/tickets/", json={
        "title": "Sem token",
        "description": "Deveria falhar",
        "category_id": cat_id,
        "priority": "baixa",
        "status": "aberto"
    })
    assert resp.status_code == 401
    assert "Not authenticated" in resp.json()["detail"]

# ========== TESTES DE REGRAS DE NEGÓCIO ==========

def test_close_ticket_without_resolution(client):
    # Setup: criar employee, agent, categoria e ticket
    client.post("/users/register", json={"username": "emp1", "email": "emp1@e.com", "password": "123", "role": "employee"})
    client.post("/users/register", json={"username": "ag1", "email": "ag1@e.com", "password": "123", "role": "agent"})
    
    cat = client.post("/categories/", json={"name": "Redes", "description": "..."}).json()
    cat_id = cat["id"]
    
    # Login employee e cria ticket
    token_emp = client.post("/users/login", data={"username": "emp1", "password": "123"}).json()["access_token"]
    ticket = client.post("/tickets/", json={
        "title": "Teste fechamento",
        "description": "Desc",
        "category_id": cat_id,
        "priority": "media",
        "status": "aberto"
    }, headers={"Authorization": f"Bearer {token_emp}"}).json()
    ticket_id = ticket["id"]
    
    # Login agent e tenta fechar sem resolução
    token_ag = client.post("/users/login", data={"username": "ag1", "password": "123"}).json()["access_token"]
    # Primeiro muda para em_andamento (transição válida)
    client.patch(f"/tickets/{ticket_id}/status", json={"status": "em_andamento"},
                 headers={"Authorization": f"Bearer {token_ag}"})
    # Tenta fechar sem resolution → deve dar 400
    resp = client.patch(f"/tickets/{ticket_id}/status", json={"status": "fechado"},
                         headers={"Authorization": f"Bearer {token_ag}"})
    assert resp.status_code == 400
    assert "resolução" in resp.json()["detail"].lower()

def test_invalid_status_transition(client):
    # Setup similar
    client.post("/users/register", json={"username": "emp2", "email": "emp2@e.com", "password": "123", "role": "employee"})
    client.post("/users/register", json={"username": "ag2", "email": "ag2@e.com", "password": "123", "role": "agent"})
    
    cat = client.post("/categories/", json={"name": "Software", "description": "..."}).json()
    cat_id = cat["id"]
    
    token_emp = client.post("/users/login", data={"username": "emp2", "password": "123"}).json()["access_token"]
    ticket = client.post("/tickets/", json={
        "title": "Teste transição",
        "description": "Desc",
        "category_id": cat_id,
        "priority": "alta",
        "status": "aberto"
    }, headers={"Authorization": f"Bearer {token_emp}"}).json()
    ticket_id = ticket["id"]
    
    token_ag = client.post("/users/login", data={"username": "ag2", "password": "123"}).json()["access_token"]
    # Tentar pular de aberto para fechado (transição inválida)
    resp = client.patch(f"/tickets/{ticket_id}/status", json={"status": "fechado", "resolution": "resolução qualquer"},
                         headers={"Authorization": f"Bearer {token_ag}"})
    assert resp.status_code == 400
    assert "transição inválida" in resp.json()["detail"].lower()

def test_reopen_ticket_clears_resolution(client):
    # Setup: criar employee, agent, categoria e ticket
    client.post("/users/register", json={"username": "emp3", "email": "emp3@e.com", "password": "123", "role": "employee"})
    client.post("/users/register", json={"username": "ag3", "email": "ag3@e.com", "password": "123", "role": "agent"})
    
    cat = client.post("/categories/", json={"name": "Infra", "description": "..."}).json()
    cat_id = cat["id"]
    
    token_emp = client.post("/users/login", data={"username": "emp3", "password": "123"}).json()["access_token"]
    ticket = client.post("/tickets/", json={
        "title": "Teste reabertura",
        "description": "Desc",
        "category_id": cat_id,
        "priority": "baixa",
        "status": "aberto"
    }, headers={"Authorization": f"Bearer {token_emp}"}).json()
    ticket_id = ticket["id"]
    
    token_ag = client.post("/users/login", data={"username": "ag3", "password": "123"}).json()["access_token"]
    # Agente muda para em_andamento e depois fecha com resolução
    client.patch(f"/tickets/{ticket_id}/status", json={"status": "em_andamento"},
                 headers={"Authorization": f"Bearer {token_ag}"})
    client.patch(f"/tickets/{ticket_id}/status", json={"status": "fechado", "resolution": "Problema resolvido"},
                 headers={"Authorization": f"Bearer {token_ag}"})
    
    # Agora reabre o ticket (fechado → aberto)
    resp = client.patch(f"/tickets/{ticket_id}/status", json={"status": "aberto"},
                         headers={"Authorization": f"Bearer {token_ag}"})
    assert resp.status_code == 200
    # Verifica se a resolução foi limpa
    assert resp.json()["resolution"] is None