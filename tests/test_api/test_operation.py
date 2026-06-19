"""pytest from AAA: Arrange, Act, Assert"""

from decimal import Decimal

from app.models import User
from app.enum import CurrencyEnum

def test_add_expense_succes(user_with_wallet, client):
    # Arrange
    user, wallet = user_with_wallet
    
    #Act
    response = client.post(
        "/api/v1/operation/expense", 
        json={
            "wallet_name": wallet.name,
            "amount": 50.0,
            "description": "food"
        }, 
        headers={"Authorization": f"Bearer {user.login}"}
    )
    
    # Assert
    
    assert response.status_code == 200
    data = response.json()
    
    # Проверяем поля OperationResponse
    assert data["wallet_id"] == wallet.id
    assert data["type"] == "expense"
    assert Decimal(str(data["amount"])) == Decimal(50.0)
    assert data["currency"] == CurrencyEnum.RUB
    assert data["category"] == "food"
    assert "id" in data
    assert "created_at" in data

 
def test_add_expense_negative_amount(user_with_wallet, client):
    # Arrange
    
    user, wallet = user_with_wallet
    
      #Act
    response = client.post(
        "/api/v1/operation/expense", 
        json={
            "wallet_name": wallet.name,
            "amount": -100.0,
            "description": "food"
        }, 
        headers={"Authorization": f"Bearer {user.login}"}
    )
    
     # Assert
    
    assert response.status_code == 422
    
def test_add_expense_empty_name(user_with_wallet, client):
    
    # Arrange
    user, wallet = user_with_wallet 
    
    #Act
    response = client.post(
        "/api/v1/operation/expense", 
        json={
            "wallet_name": "  ",
            "amount": 100.0,
            "description": "food"
        }, 
        headers={"Authorization": f"Bearer {user.login}"}
    )
    
     # Assert
    
    assert response.status_code == 422
    
    
def test_add_expense_wallet_not_exists(db_session, client):
    
    # Arrange
    
    user = User(login="test")
    db_session.add(user)
    db_session.commit()
    
    #Act
    response = client.post(
        "/api/v1/operation/expense", 
        json={
            "wallet_name": "card",
            "amount": 100.0,
            "description": "food"
        }, 
        headers={"Authorization": f"Bearer {user.login}"}
    )
    
    # Assert
    
    assert response.status_code == 404
    
    
def test_add_expense_unauthorized(db_session, client):
    
    # Arrange
 
    #Act
    response = client.post(
        "/api/v1/operation/expense", 
        json={
            "wallet_name": "card",
            "amount": 100.0,
            "description": "food"
        }, 
        headers={"Authorization": f"Bearer notexists"}
    )
    
     # Assert
    
    assert response.status_code == 401
    
    
def test_add_expense_not_enough_money(user_with_wallet, client):
    # Arrange
    user, wallet = user_with_wallet
    
    #Act
    response = client.post(
        "/api/v1/operation/expense", 
        json={
            "wallet_name": wallet.name,
            "amount": 250.0,
            "description": "food"
        }, 
        headers={"Authorization": f"Bearer {user.login}"}
    )
    
    # Assert
    
    assert response.status_code == 400
    
#TODO: Попытка создать кошелёк с уже существующим именем
#TODO:Попытка получить баланс несуществующего кошелька

# TODO: покрыть тестами остальной функционал
    