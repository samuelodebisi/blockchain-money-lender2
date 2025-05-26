# Money Lender Blockchain App

This is a Python-based blockchain application built for simulating and validating lending transactions in a decentralized finance (DeFi) setting. The project was created as part of a master's level coursework to explore transaction validation, block confirmation, and peer-to-peer mechanisms in blockchain.

## 🔍 Features

- Create, validate, and confirm lending transactions
- Blockchain integrity maintained using SHA-256 hashing
- Transaction verification via rules (non-zero amounts, no self-lending, sufficient balance)
- Group-based lending with equal contribution and RSA-based proof of participation
- Flask-based API server for easy interaction
- Timestamp validation to prevent duplicate or out-of-sequence blocks

## 🛠 Technologies Used

- Python 3.x
- Flask
- SHA-256 (hashlib)
- RSA (Cryptography)
- JSON/OpenAPI for data interaction

## 📦 Files Overview

- `money_lender_blockchain.py` – Core blockchain and block logic
- `lending_requests.py` – Lending transaction validation and handling
- `money_lender_app.py` – Flask API server for blockchain interaction
- `requirements.txt` – List of dependencies
- `how_to_run_the_project.txt` – Step-by-step usage guide

## 🚀 Getting Started

1. Clone or download this repository
2. Create a virtual environment (optional but recommended)
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the Flask server:

```bash
python money_lender_app.py
```

5. Visit the OpenAPI interface (typically at `http://localhost:5000/openapi/swagger`) to interact with the blockchain.

## ✅ Example Use Cases

- Simulate transactions between lender and borrower
- Create group-based loans
- Validate blockchain security with timestamps and hashing
- Assign cryptographic proof of participation to group lenders

## 📚 License

This project is academic in nature and intended for educational use.

---

Feel free to fork or extend the project for your own experimentation with blockchain development.
