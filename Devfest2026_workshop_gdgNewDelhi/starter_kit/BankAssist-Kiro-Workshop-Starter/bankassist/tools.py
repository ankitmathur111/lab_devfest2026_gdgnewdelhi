from .data import CUSTOMERS, BENEFICIARIES

TOOL_RISK = {
    "get_public_fee": "LOW",
    "get_balance": "LOW",
    "get_transactions": "MEDIUM",
    "create_service_request": "MEDIUM",
    "transfer_money": "HIGH",
}

def get_public_fee():
    return {"international_transfer_fee": "₹250 + applicable charges"}

def get_balance(user_id):
    customer = CUSTOMERS[user_id]
    return {"customer_id": user_id, "balance": customer["balance"]}

def get_transactions(user_id, requested_customer_id=None):
    owner = requested_customer_id or user_id
    return {"customer_id": owner, "transactions": CUSTOMERS[owner]["transactions"]}

def create_service_request(user_id, request_type):
    return {
        "request_id": "SR-" + user_id[-4:],
        "customer_id": user_id,
        "type": request_type,
        "status": "CREATED",
    }

def transfer_money(user_id, amount, beneficiary_id):
    # Deliberately simple simulation. In the guarded application this tool
    # is only reached after the policy layer; high-impact actions are normally
    # escalated before execution.
    return {
        "status": "EXECUTED_SIMULATION",
        "customer_id": user_id,
        "amount": amount,
        "beneficiary_id": beneficiary_id,
    }
