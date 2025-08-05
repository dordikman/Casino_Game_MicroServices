
## 🚀 How to Run the Project

### Prerequisites
- **Docker Desktop** installed and running
- Port **8000** available

### 🐳 Docker-Based Testing (Recommended)

#### Run Positive Tests:
```bash
docker-compose up --build casino-server test-positive
```

#### Run Negative Tests:
```bash
docker-compose up --build casino-server test-negative
```

#### Run End-to-End Tests:
```bash
docker-compose up --build casino-server test-e2e
```

#### Stop All Services:
```bash
docker-compose down
```

### 📊 View Test Results

#### HTML Reports (Generated automatically):
```bash
# Open in browser:
start reports\positive_report.html
start reports\negative_report.html
start reports\e2e_report.html
```

#### Console Output:
- Real-time test results in terminal
- Server logs showing API interactions
- Exit codes: 0 = success, 1 = failure

### 🔧 Local Development (Alternative)

#### 1. Install Dependencies:
```bash
pip install -r requirements.txt
```

#### 2. Start Server:
```bash
python app.py
```

#### 3. Run Tests (in separate terminal):
```bash
# Positive tests
pytest tests/test_positive.py -v

# Negative tests  
pytest tests/test_negative.py -v

# E2E tests with logging
pytest tests/test_e2e.py -s -v --log-cli-level=INFO

# All tests with HTML report
pytest tests/ -v --html=reports/all_tests.html --self-contained-html
```

## 🎯 What Each Test Category Does

### **Positive Tests** (Expected to PASS)
- `test_win_lose_outcome_displays_correct_message` - Game outcome validation
- `test_user_balance_update` - Balance update functionality
- `test_place_bet` - Bet placement and balance deduction
- `test_payout_success` - Complete game flow with conditional payout
- `test_slot_spin` - Slot machine mechanics

### **Negative Tests** (Expected to FAIL - Demonstrates Server Bugs)
- `test_negative_bet_amount` - Rejects negative bet amounts
- `test_notification_missing_message` - Validates required fields
- `test_update_balance_missing_new_balance` - Parameter validation
- `test_payout_with_zero_win_amount` - Business rule enforcement
- `test_spin_with_maximum_bet_amount_edge_case` - Edge case boundary testing

### 🔄 **E2E Tests** (Integration Testing)
- `test_complete_end_to_end_game_flow` - Full game workflow validation


## Assumptions 
- because there was no built in server or specific instructions to build one i decided to use a mock server with Flask.
- i didnt add any support for new user creation as the system should work exactly the same, if a new endpoint is added we can just add it to api_client.py
- the server has no logic except the fact that i needed to check a valid win scenario so i made sure the server knows that a win must have 3 matched symbols.
- no minimum or maximum bet restrictions.
- used an in memory db, in a production based system the server relies on out source db.
- i tried to keep it as simple as i could, yet using a design that will be maintainable , readable and flexiable for future use.

## time taken- 2 days