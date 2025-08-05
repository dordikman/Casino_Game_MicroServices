import requests
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def make_request(endpoint, method, **kwargs):
    url = f"{API_BASE_URL}{endpoint}"
    try:
        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        return response
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Request failed: {e}")

class UserService:
    def get_balance(self, userId):
        return make_request(endpoint="/user/balance", method="GET", params={"userId": userId})

    def update_balance(self, userId, newBalance):
        return make_request(endpoint="/user/update-balance", method="POST", json={"userId": userId, "newBalance": newBalance})

class PaymentService:
    def place_bet(self, userId, betAmount):
        return make_request(endpoint="/payment/placeBet", method="POST", json={"userId": userId, "betAmount": betAmount})
    
    def payout(self, userId, transactionId, winAmount):
        return make_request(endpoint="/payment/payout", method="POST", json={"userId": userId, "transactionId": transactionId, "winAmount": winAmount})

class GameService:
    def spin(self, userId, betAmount, transactionId):
        return make_request(endpoint="/slot/spin", method="POST", json={"userId": userId, "betAmount": betAmount, "transactionId": transactionId})

class NotificationService:
    def send_notification(self, userId, transactionId, message):
        return make_request(endpoint="/notify", method="POST", json={"userId": userId, "transactionId": transactionId, "message": message})


