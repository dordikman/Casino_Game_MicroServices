# mock server 

from flask import Flask, request, jsonify

app = Flask(__name__)

players = [{"userId": 123, "balance": 150.00, "currency": "USD"}]
transactions = []
spin_results = []
notifications = []


@app.route('/user/balance', methods=['GET'])
def get_balance():
    userId = request.args.get('userId', type=int)
    user = next((p for p in players if p['userId'] == userId), None)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({
        "userId": user['userId'],
        "balance": user['balance'],
        "currency": user['currency']
    })


@app.route('/user/update-balance', methods=['POST'])
def update_balance():
    data = request.get_json()
    userId = data.get('userId')
    newBalance = data.get('newBalance')
    
    # Find user in players list
    user = next((p for p in players if p['userId'] == userId), None)
    
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    # Update existing user's balance
    user['balance'] = newBalance
    
    return jsonify({
        "userId": user['userId'],
        "balance": user['balance'],
        "currency": user['currency']
    })



@app.route('/payment/placeBet', methods=['POST'])
def place_bet():
    data = request.get_json()
    userId = data.get('userId')
    betAmount = data.get('betAmount')
    
    # Find user in players list
    user = next((p for p in players if p['userId'] == userId), None)
    
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    # Check if user has enough balance
    if user['balance'] < betAmount:
        return jsonify({"error": "Insufficient balance"}), 400
    
    
    import random
    transactionId = f"txn_{random.randint(100, 999)}"
    
   
    user['balance'] -= betAmount
    
    # Create transaction record
    transaction = {
        "transactionId": transactionId,
        "userId": userId,
        "betAmount": betAmount,
        "status": "SUCCESS"
    }
    transactions.append(transaction)
    
    return jsonify({
        "userId": userId,
        "transactionId": transactionId,
        "status": "SUCCESS",
        "newBalance": user['balance']
    })


@app.route('/payment/payout', methods=['POST'])
def payout():
    data = request.get_json()
    userId = data.get('userId')
    transactionId = data.get('transactionId')
    winAmount = data.get('winAmount')
    
    # Find user in players list
    user = next((p for p in players if p['userId'] == userId), None)
    
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    # Find transaction in transactions list
    transaction = next((t for t in transactions if t['transactionId'] == transactionId), None)
    
    if transaction is None:
        return jsonify({"error": "Transaction not found"}), 404
    
    
    user['balance'] += winAmount
    
   
    transaction['winAmount'] = winAmount
    transaction['payoutStatus'] = 'PAID'
    
    return jsonify({
        "userId": userId,
        "transactionId": transactionId,  
        "status": "SUCCESS",
        "newBalance": user['balance']
    })


@app.route('/slot/spin', methods=['POST'])
def spin():
    data = request.get_json()
    userId = data.get('userId')
    betAmount = data.get('betAmount')
    transactionId = data.get('transactionId')
    
    
    user = next((p for p in players if p['userId'] == userId), None)
    
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    # Find transaction in transactions list
    transaction = next((t for t in transactions if t['transactionId'] == transactionId), None)
    
    if transaction is None:
        return jsonify({"error": "Transaction not found"}), 404
    
    # Slot machine logic - determine win or lose
    import random
    reels = ["Cherry", "Bell", "Seven", "Bar", "Lemon"]
    spin_result = [random.choice(reels) for _ in range(3)]
    
    # Determine outcome based on combination
    # WIN condition: Only three of a kind
    if spin_result[0] == spin_result[1] == spin_result[2]:
        outcome = "WIN"
        if spin_result[0] == "Cherry":
            winAmount = betAmount * 10  
        elif spin_result[0] == "Seven":
            winAmount = betAmount * 5   
        else:
            winAmount = betAmount * 3   
        message = f"Congratulations! You won ${winAmount}!"
    else:
        # All other combinations are LOSE
        outcome = "LOSE"
        winAmount = 0
        message = "Better luck next time!"
    
    # Create spin result record
    spin_result_record = {
        "transactionId": transactionId,
        "userId": userId,
        "outcome": outcome,
        "winAmount": winAmount,
        "reels": spin_result,
        "message": message
    }
    spin_results.append(spin_result_record)
    
    return jsonify({
        "userId": userId,
        "outcome": outcome,
        "winAmount": winAmount,
        "reels": spin_result,
        "message": message
    })


@app.route('/notify', methods=['POST'])
def send_notification():
    data = request.get_json()
    userId = data.get('userId')
    transactionId = data.get('transactionId')
    message = data.get('message')
    
    # Find user in players list
    user = next((p for p in players if p['userId'] == userId), None)
    
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    
    transaction = next((t for t in transactions if t['transactionId'] == transactionId), None)
    
    if transaction is None:
        return jsonify({"error": "Transaction not found"}), 404
    
    
    import random
    notificationId = f"notif_{random.randint(100, 999)}"
    
    # Create notification record
    notification = {
        "notificationId": notificationId,
        "userId": userId,
        "transactionId": transactionId,
        "message": message,
        "status": "SENT"
    }
    notifications.append(notification)
    
    return jsonify({
        "status": "SENT",
        "notificationId": notificationId
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)