import pytest
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_complete_end_to_end_game_flow(user_service, payment_service, game_service, notification_service, helpers, test_data):
    # Use test data instead of hard-coded values
    scenario = test_data["scenarios"]["standard_game"]
    user_id = scenario["user_id"]
    bet_amount = scenario["bet_amount"]
    
    logger.info("Starting E2E Game Flow Test")
    
    # STEP 1: Get initial balance
    initial_balance = helpers.get_user_balance(user_service, user_id)
    assert initial_balance >= bet_amount, f"Insufficient balance: ${initial_balance} < ${bet_amount}"
    logger.info(f"Initial balance: ${initial_balance}")
    
    # STEP 2: Place bet
    transaction_id, balance_after_bet = helpers.place_bet_and_verify(payment_service, user_service, user_id, bet_amount)
    logger.info(f"Bet placed: ${bet_amount} | Transaction ID: {transaction_id}")
    
    # STEP 3: Spin slot machine
    spin_data = helpers.perform_spin_and_get_outcome(game_service, user_id, bet_amount, transaction_id)
    
    outcome = spin_data["outcome"]
    win_amount = spin_data["winAmount"]
    reels = spin_data["reels"]
    message = spin_data["message"]
    
    logger.info(f"Spin result: {outcome} | Reels: {reels} | Win: ${win_amount}")
    
    
    if outcome == "WIN":
        won = helpers.process_payout_if_win(payment_service, user_service, user_id, transaction_id, spin_data)
        assert won == True, "Helper should have processed the payout"
        final_balance = helpers.get_user_balance(user_service, user_id)
        logger.info(f"Payout processed: ${win_amount}")
    else:
        final_balance = balance_after_bet
    
    # STEP 5: Send notification
    notification_response = helpers.send_notification_and_verify(notification_service, user_id, transaction_id, message)
    notification_id = notification_response.json()["notificationId"]
    
    if outcome == "WIN":
        expected_final = initial_balance - bet_amount + win_amount
    else:
        expected_final = initial_balance - bet_amount
    
    assert final_balance == expected_final, f"Balance calculation error: {final_balance} != {expected_final}"
    
    # Calculate change
    net_change = final_balance - initial_balance
    net_change_str = f"+${net_change}" if net_change >= 0 else f"-${abs(net_change)}"
    
    # Final summary
    logger.info(f"E2E Test Complete: {outcome} | Net: {net_change_str} | Final Balance: ${final_balance}")