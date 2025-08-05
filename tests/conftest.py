from tests.api_client import UserService, PaymentService, GameService, NotificationService
from tests.test_data import TEST_DATA, get_user, get_bet_amount, get_balance, get_scenario, get_negative_data
import pytest


class TestHelpers:
    @staticmethod
    def get_user_balance(user_service, user_id=None):
        if user_id is None:
            user_id = get_user("valid_user")
        response = user_service.get_balance(user_id)
        return response.json()["balance"]

    @staticmethod
    def verify_balance_equals(user_service, user_id, expected_balance):
        current_balance = TestHelpers.get_user_balance(user_service, user_id)
        assert current_balance == expected_balance
        return current_balance

    @staticmethod
    def verify_balance_decreased(user_service, user_id, initial_balance, decrease_amount):
        expected_balance = initial_balance - decrease_amount
        TestHelpers.verify_balance_equals(user_service, user_id, expected_balance)

    @staticmethod
    def verify_balance_increased(user_service, user_id, initial_balance, increase_amount):
        expected_balance = initial_balance + increase_amount
        TestHelpers.verify_balance_equals(user_service, user_id, expected_balance)

    @staticmethod
    def place_bet_and_verify(payment_service, user_service, user_id, bet_amount):
        initial_balance = TestHelpers.get_user_balance(user_service, user_id)
        
        bet_response = payment_service.place_bet(user_id, bet_amount)
        assert bet_response.status_code == 200
        
        bet_data = bet_response.json()
        assert bet_data["status"] == "SUCCESS"
        assert bet_data["newBalance"] == initial_balance - bet_amount
        
        TestHelpers.verify_balance_decreased(user_service, user_id, initial_balance, bet_amount)
        
        return bet_data["transactionId"], bet_data["newBalance"]

    @staticmethod
    def perform_spin_and_get_outcome(game_service, user_id, bet_amount, transaction_id):
        spin_response = game_service.spin(user_id, bet_amount, transaction_id)
        assert spin_response.status_code == 200
        
        spin_data = spin_response.json()
        assert "outcome" in spin_data
        assert "reels" in spin_data
        assert "message" in spin_data
        
        reels = spin_data["reels"]
        outcome = spin_data["outcome"]
        
        if reels[0] == reels[1] == reels[2]:  # Three of a kind
            assert outcome == "WIN", f"Three of a kind {reels} should be WIN, got {outcome}"
            assert spin_data["winAmount"] > 0, "WIN should have winAmount > 0"
            assert "Congratulations" in spin_data["message"], "WIN should have congratulations message"
        else:  # LOSE
            assert outcome == "LOSE", f"Non-matching reels {reels} should be LOSE, got {outcome}"
            assert spin_data["winAmount"] == 0, "LOSE should have winAmount = 0"
            assert "Better luck next time" in spin_data["message"], "LOSE should have appropriate message"
        
        return spin_data

    @staticmethod
    def process_payout_if_win(payment_service, user_service, user_id, transaction_id, outcome_data):
        if outcome_data["outcome"] == "WIN":
            win_amount = outcome_data["winAmount"]
            current_balance = TestHelpers.get_user_balance(user_service, user_id)
            
            payout_response = payment_service.payout(user_id, transaction_id, win_amount)
            assert payout_response.status_code == 200
            assert payout_response.json()["status"] == "SUCCESS"
            
            TestHelpers.verify_balance_increased(user_service, user_id, current_balance, win_amount)
            return True
        return False

    @staticmethod
    def send_notification_and_verify(notification_service, user_id, transaction_id, message):
        notification_response = notification_service.send_notification(user_id, transaction_id, message)
        assert notification_response.status_code == 200
        assert notification_response.json()["status"] == "SENT"
        return notification_response


@pytest.fixture
def helpers():
    return TestHelpers()

@pytest.fixture
def test_data():
    return TEST_DATA

@pytest.fixture
def user_service():
    return UserService()

@pytest.fixture
def payment_service():
    return PaymentService()

@pytest.fixture
def game_service():
    return GameService()

@pytest.fixture
def notification_service():
    return NotificationService()



