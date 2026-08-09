"""REST API routes for accounts."""

from flask import jsonify, request

from service.models import Account, db


def register_routes(app):
    """Register REST endpoints."""

    @app.get("/")
    def health():
        return jsonify({"service": "accounts", "status": "ok"})

    @app.post("/api/accounts")
    def create_account():
        data = request.get_json(silent=True) or {}
        required = ("name", "email")
        missing = [field for field in required if not data.get(field)]
        if missing:
            return jsonify({"error": f"Missing required field(s): {', '.join(missing)}"}), 400

        if Account.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Account with that email already exists"}), 409

        account = Account(
            name=data["name"],
            email=data["email"],
            address=data.get("address"),
        )
        db.session.add(account)
        db.session.commit()
        return jsonify(account.to_dict()), 201

    @app.get("/api/accounts")
    def list_accounts():
        return jsonify([account.to_dict() for account in Account.query.order_by(Account.id).all()])

    @app.get("/api/accounts/<int:account_id>")
    def read_account(account_id):
        account = db.session.get(Account, account_id)
        if account is None:
            return jsonify({"error": "Account not found"}), 404
        return jsonify(account.to_dict())

    @app.put("/api/accounts/<int:account_id>")
    def update_account(account_id):
        account = db.session.get(Account, account_id)
        if account is None:
            return jsonify({"error": "Account not found"}), 404

        data = request.get_json(silent=True) or {}
        if "name" in data:
            account.name = data["name"]
        if "email" in data:
            duplicate = Account.query.filter(
                Account.email == data["email"], Account.id != account.id
            ).first()
            if duplicate:
                return jsonify({"error": "Account with that email already exists"}), 409
            account.email = data["email"]
        if "address" in data:
            account.address = data["address"]

        db.session.commit()
        return jsonify(account.to_dict())

    @app.delete("/api/accounts/<int:account_id>")
    def delete_account(account_id):
        account = db.session.get(Account, account_id)
        if account is None:
            return jsonify({"error": "Account not found"}), 404
        db.session.delete(account)
        db.session.commit()
        return "", 204
