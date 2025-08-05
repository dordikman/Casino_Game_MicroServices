import pytest


def test_negative_bet_amount(payment_service, user_service, helpers, test_data):
    user_id = test_data["users"]["valid_user"]
    negative_bet_amount = test_data["negative_data"]["negative_bet"]
    
    initial_balance = helpers.get_user_balance(user_service, user_id)
    bet_response = payment_service.place_bet(user_id, negative_bet_amount)
    
    assert bet_response.status_code != 200, "Negative bet amount should be rejected"
    assert bet_response.status_code in [400, 422], f"Expected 400 or 422, got {bet_response.status_code}"
    
    error_data = bet_response.json()
    assert "error" in error_data, "Response should have error message"
    
    helpers.verify_balance_equals(user_service, user_id, initial_balance)


def test_notification_missing_message(payment_service, notification_service, test_data):
    user_id = test_data["users"]["valid_user"]
    bet_amount = test_data["bet_amounts"]["large"]
    none_message = test_data["negative_data"]["none_message"]
    
    # Place bet to get valid transaction ID
    bet_response = payment_service.place_bet(user_id, bet_amount)
    assert bet_response.status_code == 200
    transaction_id = bet_response.json()["transactionId"]
    
    # Attempt to send notification with None message
    response = notification_service.send_notification(user_id, transaction_id, none_message)
    
    assert response.status_code != 200, "Missing message field should be rejected"
    assert response.status_code in [400, 422], f"Expected 400 or 422, got {response.status_code}"
    
    error_data = response.json()
    assert "error" in error_data, "Response should contain error message"


def test_update_balance_missing_new_balance(user_service, helpers, test_data):
    user_id = test_data["users"]["valid_user"]
    none_balance = test_data["negative_data"]["none_balance"]
    
    initial_balance = helpers.get_user_balance(user_service, user_id)
    
    try:
        # Attempt to update balance with None
        response = user_service.update_balance(user_id, none_balance)
        
        # Verify error response
        assert response.status_code != 200, "Missing newBalance parameter should be rejected"
        assert response.status_code in [400, 422], f"Expected 400 or 422, got {response.status_code}"
        
        error_data = response.json()
        assert "error" in error_data, "Response should contain error message"
    finally:
        # restore balance
        user_service.update_balance(user_id, initial_balance)


def test_payout_with_zero_win_amount(payment_service, user_service, helpers, test_data):
    user_id = test_data["users"]["valid_user"]
    bet_amount = test_data["bet_amounts"]["medium"]
    zero_win = test_data["negative_data"]["zero_win"]
    
    # Ensure user has valid balance
    current_balance = helpers.get_user_balance(user_service, user_id)
    if current_balance is None or current_balance < bet_amount:
        valid_balance = test_data["balances"]["medium"]  # 150.00
        user_service.update_balance(user_id, valid_balance)
    
    # Place bet to get valid transaction ID
    bet_response = payment_service.place_bet(user_id, bet_amount)
    assert bet_response.status_code == 200
    transaction_id = bet_response.json()["transactionId"]
    
    initial_balance = helpers.get_user_balance(user_service, user_id)
    
    payout_response = payment_service.payout(user_id, transaction_id, zero_win)
    
    assert payout_response.status_code != 200, "Zero win amount payout should be rejected"
    assert payout_response.status_code in [400, 422], f"Expected 400 or 422, got {payout_response.status_code}"
    
    error_data = payout_response.json()
    assert "error" in error_data, "Response should contain error message"
    
    helpers.verify_balance_equals(user_service, user_id, initial_balance)



def test_spin_with_maximum_bet_amount_edge_case(payment_service, game_service, user_service, helpers, test_data):
    # NEGATIVE EDGE CASE
    user_id = test_data["users"]["valid_user"]
    normal_bet = test_data["bet_amounts"]["small"]
    excessive_bet = test_data["negative_data"]["excessive_bet"]
    
    # Ensure user has valid balance 
    current_balance = helpers.get_user_balance(user_service, user_id)
    if current_balance is None or current_balance < normal_bet:
        valid_balance = test_data["balances"]["medium"]
        user_service.update_balance(user_id, valid_balance)
    
    # Setup: Place a normal bet first to get valid transaction
    transaction_id, _ = helpers.place_bet_and_verify(payment_service, user_service, user_id, normal_bet)
    
    # Attempt to spin with excessive amount
    maximum_bet_amount = excessive_bet
    
    spin_response = game_service.spin(user_id, maximum_bet_amount, transaction_id)
    
    # Should return error status
    assert spin_response.status_code != 200, "Spin with mismatched bet amount should be rejected"
    assert spin_response.status_code in [400, 422], f"Expected 400 or 422, got {spin_response.status_code}"
    
    error_data = spin_response.json()
    assert "error" in error_data, "Response should contain error message"















