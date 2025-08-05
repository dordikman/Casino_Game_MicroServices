# Casino Game Microservices - Test Design & Documentation

## Overview
This document contains the test design, test cases, and debugging solutions for the Casino Game Microservices QA automation exam.

## Test Design

The test automation framework consists of 6 main components designed to provide comprehensive coverage of the Casino Game Microservices:

### 1. **api_client.py** - Service Layer (Page Object Model Pattern)
This file consists of 4 different classes, each representing a microservice:
- **UserService**: Handles balance retrieval and updates
- **PaymentService**: Manages betting transactions and payouts
- **GameService**: Controls slot machine spin functionality
- **NotificationService**: Handles user notifications

The goal is to define all API requests in one place, allowing other testers to add more endpoints without changing any structure or logic. This follows the Page Object Model (POM) pattern for API testing.

### 2. **conftest.py** - Test Infrastructure and Helper Functions
This file is a common pytest practice that uses important pytest fixtures. It contains:
- **Service Fixtures**: Provides instances of all service classes
- **TestHelpers Class**: Contains reusable validation methods and business logic
- **test_data Fixture**: Provides access to centralized test data

The goal is not to duplicate code in the test structure and to define helper functions to maintain SOLID principles.

### 3. **test_data.py** - Centralized Data Management
Contains all test data organized in scenarios, user information, bet amounts, and negative test cases. This data-driven approach allows easy modification of test inputs without changing test logic.

### 4. **test_positive.py** - Happy Path Testing
Uses conftest and api_client fixtures. The fixtures from conftest pass as function input along with api_client services. Contains 5 comprehensive positive test cases validating successful system operations.

### 5. **test_negative.py** - Error Handling and Validation Testing  
Uses conftest and api_client fixtures. Contains 5 negative test cases that validate system error handling, input validation, and business rule enforcement.

### 6. **test_e2e.py** - End-to-End Integration Testing
Contains comprehensive end-to-end flow testing that validates the complete game workflow across all microservices with detailed logging.

## Detailed Test Case Documentation

### **Positive Test Cases** (test_positive.py)

#### 1. `test_win_lose_outcome_displays_correct_message`
**Purpose**: Validates that game outcome messages correctly match the spin results  
**Business Rule**: WIN/LOSE messages must be consistent with actual game outcome  
**Test Flow**:
- Places a bet using small_bet_game scenario (10.20 amount)
- Performs slot spin with transaction ID
- Validates message content matches outcome (WIN shows congratulations, LOSE shows better luck)
- Uses helper function for business rule enforcement (3-of-a-kind = WIN)

#### 2. `test_user_balance_update`
**Purpose**: Verifies user balance update functionality works correctly  
**Business Rule**: Balance updates must be accurate and reflected immediately  
**Test Flow**:
- Updates user balance to test amount (200.50)
- Verifies balance change through helper function
- Validates response structure (userId, currency)
- Ensures data consistency across the system

#### 3. `test_place_bet`
**Purpose**: Tests successful bet placement and balance deduction  
**Business Rule**: Bets must deduct correct amount and generate valid transaction IDs  
**Test Flow**:
- Places bet using edge_case_game scenario (15.00 amount)
- Verifies balance is correctly deducted
- Validates transaction ID generation
- Ensures transaction integrity through helper functions

#### 4. `test_payout_success`
**Purpose**: Validates complete game flow with conditional payout processing  
**Business Rule**: Payouts only occur for WIN outcomes and must update balance correctly  
**Test Flow**:
- Executes full game workflow using high_stakes_game scenario (110.00 amount)
- Places bet → Spins slot → Processes conditional payout → Sends notification
- Validates each step with appropriate helper functions
- Ensures end-to-end transaction consistency

#### 5. `test_slot_spin`
**Purpose**: Tests slot machine spin mechanics and response data structure  
**Business Rule**: Spin must return valid reels, outcome, and win amount data  
**Test Flow**:
- Places bet and gets transaction ID
- Performs slot spin with edge_case_game scenario
- Validates response structure (userId, reels array, winAmount type)
- Ensures proper data types and game logic validation

### **Negative Test Cases** (test_negative.py)

#### 1. `test_negative_bet_amount`
**Purpose**: Validates rejection of negative bet amounts  
**Business Rule**: System must reject invalid bet amounts with proper error codes  
**Test Flow**:
- Attempts to place bet with negative amount (-25.00)
- Expects 400/422 error status code
- Validates error message structure
- Ensures balance remains unchanged after failed transaction

#### 2. `test_notification_missing_message`
**Purpose**: Tests validation when required message field is missing  
**Business Rule**: Notification service must validate required fields  
**Test Flow**:
- Places valid bet to get transaction ID
- Attempts to send notification with None message
- Expects validation error (400/422 status)
- Validates proper error response structure

#### 3. `test_update_balance_missing_new_balance`
**Purpose**: Tests parameter validation for balance updates  
**Business Rule**: Balance update must require newBalance parameter  
**Test Flow**:
- Attempts to update balance with None value
- Expects parameter validation error
- Validates error response contains proper message
- Ensures original balance remains unchanged

#### 4. `test_payout_with_zero_win_amount`
**Purpose**: Validates business rule enforcement for zero payouts  
**Business Rule**: Zero win amount payouts should be rejected as invalid  
**Test Flow**:
- Places valid bet and gets transaction ID
- Attempts payout with zero win amount
- Expects business rule validation error
- Ensures balance integrity is maintained

#### 5. `test_spin_with_maximum_bet_amount_edge_case`
**Purpose**: Tests system limits with excessive bet amounts (Edge Case)  
**Business Rule**: System should reject unreasonably large bet amounts  
**Test Flow**:
- Places normal bet first to get valid transaction
- Attempts spin with excessive bet amount (99999.99)
- Validates mismatched amount rejection
- Tests edge case boundary conditions

### **End-to-End Test** (test_e2e.py)

#### `test_complete_end_to_end_game_flow`
**Purpose**: Validates complete game round from start to finish  
**Business Rule**: Full game workflow must maintain data consistency across all services  
**Test Flow**:
1. **Initial Setup**: Get user balance and validate sufficient funds
2. **Bet Placement**: Place bet and verify transaction creation
3. **Game Execution**: Spin slot machine and get outcome
4. **Conditional Processing**: Process payout only if outcome is WIN
5. **Notification**: Send outcome notification to user
6. **Final Validation**: Verify balance calculations and transaction consistency

**Logging**: Provides detailed step-by-step execution information for debugging and monitoring

## Test Execution Strategy

### **Data-Driven Approach**
All tests use centralized test data from `test_data.py`:
- **Scenarios**: Different game types (standard, high-stakes, small-bet, edge-case)
- **User Data**: Valid and invalid user IDs for testing
- **Bet Amounts**: Range from minimum (0.01) to excessive (99999.99)
- **Negative Data**: Invalid inputs for comprehensive error testing

### **Helper Function Utilization**
Tests leverage `TestHelpers` class methods:
- `get_user_balance()`: Retrieves current user balance
- `place_bet_and_verify()`: Handles bet placement with validation
- `perform_spin_and_get_outcome()`: Manages spin logic and business rule enforcement
- `process_payout_if_win()`: Conditional payout processing
- `send_notification_and_verify()`: Notification handling with verification

### **Business Rule Enforcement**
- **WIN Condition**: Only three-of-a-kind combinations (Cherry-Cherry-Cherry, Seven-Seven-Seven, etc.)
- **LOSE Condition**: All other combinations including two-of-a-kind
- **Balance Integrity**: All transactions must maintain accurate balance calculations
- **Transaction Consistency**: Transaction IDs must be consistent across services


## Code Debugging 
The current code is not maintainable or readable. The best practice is to use the Page Object Model.
There are 4 major problems with the current code:
## 1. not following solid code prinicples
There is too much logic in one function; therefore, the code is not maintainable.
I would separate the login process into a dedicated class that handles the logic for the login page.
Currently, the function navigates to the URL, enters data into the fields, and clicks the login button all in one place.

## 2. not using fixtures
Using fixtures allows code reusability, manages browser setup and teardown, and prevents code duplication across other tests.

## 3. Assertion against hard‑coded text
The validation of a successful login attempt is incorrect. If the text changes, the test will fail unnecessarily.
A better approach is to use unique identifiers, such as verifying a designated URL after a successful login or checking for the presence of a logout button.

## 4. no explicit waits 
The code assumes that elements will always be visible. This is not true, especially when testing across multiple platforms.
Some browsers may be slower, so the best practice is to use explicit waits and check if the elements are visible and clickable before interacting with them.

## rewriting the code with python
i will define a class called LogIn inside a folder called pages, a folder called tests and inside a file called test_login and a conftest file.

LogIn class : 
class LogIn:
    def __init__(self, driver):
        self.driver = driver
        self.username_field = (By.ID, "username")  #depends
        self.password_field = (By.ID, "password")  #depends
        self.login_button = (By.ID, "login_button") #depends

    def navigate(self):
        self.driver.get("https://example.com/login")

    def enter_username(self, username):
        username_element = self.wait.until(
            EC.presence_of_element_located(self.username_field)
        )
        username_element.send_keys(username)

    def enter_password(self, password):
        password_element = self.wait.until(
            EC.presence_of_element_located(self.password_field)
        )
        password_field.send_keys(password)

    def click_login_button(self):
        login_button_element = self.wait.until(
            EC.presence_of_element_located(self.login_button)
        )
        login_button_element.click()

conftest:
pytest.fixture(scope= "session")
def chrome_driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

pytest.fixture(scope= "session")
def login_page(chrome_driver):
    return LogIn(driver)


test_login:
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def test_successful_login(login_page):
    try:
        login_page.navigate()
        login_page.enter_username("name")
        login_page.enter_password("password")
        login_page.click_login_button()
        assert driver.current_url == "https://example.com/MyAccount"
        logger.info("login succsseful") 
    except Exception as e:
        logger.info("log in failed")




