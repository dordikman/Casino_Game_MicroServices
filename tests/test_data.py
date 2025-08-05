
TEST_DATA = {
    # User data
    "users": {
        "valid_user": 123,
        "invalid_user": 999,
        "another_user": 456
    },
    
    # Bet amounts for different test scenarios
    "bet_amounts": {
        "minimum": 0.01,
        "very_small": 1.00,
        "small": 10.00,
        "medium": 25.00,
        "large": 50.00,
        "very_large": 100.00,
        "maximum": 999.99,
        "excessive": 99999.99  # For negative tests
    },
    
    # Balance amounts
    "balances": {
        "low": 5.00,
        "medium": 150.00,
        "high": 500.00,
        "updated_test": 200.50
    },
    
    # Currency
    "currency": "USD",
    
    # Expected messages
    "messages": {
        "win_keyword": "Congratulations",
        "lose_keyword": "Better luck next time"
    },
    
    
    # Test scenarios - predefined combinations
    "scenarios": {
        "standard_game": {
            "user_id": 123,
            "bet_amount": 25.00
        },
        "small_bet_game": {
            "user_id": 123,
            "bet_amount": 10.20
        },
        "high_stakes_game": {
            "user_id": 123,
            "bet_amount": 110.00
        },
        "minimum_bet_game": {
            "user_id": 123,
            "bet_amount": 0.01
        },
        "edge_case_game": {
            "user_id": 123,
            "bet_amount": 15.00
        }
    },
    
    "negative_data": {
        "negative_bet": -25.00,
        "zero_win": 0,
        "none_message": None,
        "none_balance": None,
        "fake_transaction": "txn_999999",
        "excessive_bet": 99999.99
    }
}

def get_user(user_type="valid_user"):
    """Get user ID by type"""
    return TEST_DATA["users"][user_type]

def get_bet_amount(amount_type="medium"):
    """Get bet amount by type"""
    return TEST_DATA["bet_amounts"][amount_type]

def get_balance(balance_type="medium"):
    """Get balance amount by type"""
    return TEST_DATA["balances"][balance_type]

def get_scenario(scenario_name):
    """Get complete test scenario"""
    return TEST_DATA["scenarios"][scenario_name]

def get_negative_data(data_type):
    """Get negative test data"""
    return TEST_DATA["negative_data"][data_type]