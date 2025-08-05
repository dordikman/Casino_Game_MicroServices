import pytest


def test_win_lose_outcome_displays_correct_message(payment_service, game_service, notification_service, helpers, test_data):
    # Use test data
    scenario = test_data["scenarios"]["small_bet_game"]
    user_id = scenario["user_id"]
    bet_amount = scenario["bet_amount"]
    
    # Place bet
    bet_response = payment_service.place_bet(user_id, bet_amount)
    assert bet_response.status_code == 200
    transaction_id = bet_response.json()["transactionId"]
    spin_data = helpers.perform_spin_and_get_outcome(game_service, user_id, bet_amount, transaction_id)


def test_user_balance_update(user_service, helpers, test_data):
    # Use test data instead of hard-coded values
    user_id = test_data["users"]["valid_user"]
    new_balance = test_data["balances"]["updated_test"]
    currency = test_data["currency"]
    
    response = user_service.update_balance(user_id, new_balance)
    assert response.status_code == 200
    helpers.verify_balance_equals(user_service, user_id, new_balance)
    data = response.json()
    assert data["userId"] == user_id
    assert data["currency"] == currency


def test_place_bet(payment_service, user_service, helpers, test_data):
    # Use test data
    scenario = test_data["scenarios"]["edge_case_game"]
    user_id = scenario["user_id"]
    bet_amount = scenario["bet_amount"]
    
    transaction_id, new_balance = helpers.place_bet_and_verify(payment_service, user_service, user_id, bet_amount)
    assert transaction_id is not None


def test_payout_success(payment_service, game_service, user_service, notification_service, helpers, test_data):
    # Use test data
    scenario = test_data["scenarios"]["high_stakes_game"]
    user_id = scenario["user_id"]
    bet_amount = scenario["bet_amount"]
    
    transaction_id, _ = helpers.place_bet_and_verify(payment_service, user_service, user_id, bet_amount)
    spin_data = helpers.perform_spin_and_get_outcome(game_service, user_id, bet_amount, transaction_id)
    helpers.process_payout_if_win(payment_service, user_service, user_id, transaction_id, spin_data)
    helpers.send_notification_and_verify(notification_service, user_id, transaction_id, spin_data["message"])


def test_slot_spin(payment_service, game_service, helpers, test_data):
    # Use test data
    scenario = test_data["scenarios"]["edge_case_game"]
    user_id = scenario["user_id"]
    bet_amount = scenario["bet_amount"]
    
    # Place bet
    bet_response = payment_service.place_bet(user_id, bet_amount)
    transaction_id = bet_response.json()["transactionId"]
    spin_data = helpers.perform_spin_and_get_outcome(game_service, user_id, bet_amount, transaction_id)
    
    assert spin_data["userId"] == user_id
    assert len(spin_data["reels"]) == 3
    assert isinstance(spin_data["winAmount"], (int, float))