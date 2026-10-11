CUSTOMERS = {
    "CUST-1001": {
        "name": "Aarav Sharma",
        "balance": 184250.75,
        "transactions": [
            {"id": "TX-101", "amount": -2400, "description": "Utility bill"},
            {"id": "TX-102", "amount": 125000, "description": "Salary credit"},
            {"id": "TX-103", "amount": -1800, "description": "Groceries"},
        ],
    },
    "CUST-2002": {
        "name": "Meera Iyer",
        "balance": 92150.25,
        "transactions": [
            {"id": "TX-201", "amount": -5200, "description": "Travel"},
            {"id": "TX-202", "amount": 85000, "description": "Salary credit"},
        ],
    },
}

BENEFICIARIES = {
    "CUST-1001": {
        "ABC123": {"name": "Rohan", "new": False},
        "NEW999": {"name": "New Beneficiary", "new": True},
    }
}
