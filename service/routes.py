"""REST routes for the Customer Accounts service."""

from flask import abort, jsonify, make_response, request

from service.models import Account, DataValidationError, db


def _account_payload(account):
    return account.serialize()


def _create_account():
    """Create an Account from a JSON request."""
    if request.content_type != "application/json":
        abort(415, description="Content-Type must be application/json")

    account = Account()
    try:
        account.deserialize(request.get_json(silent=True))
    except DataValidationError as error:
        abort(400, description=str(error))

    if Account.find_by_email(account.email):
        abort(409, description="Account with that email already exists")

    account.create()
    response = make_response(jsonify(_account_payload(account)), 201)
    response.headers["Location"] = f"/accounts/{account.id}"
    return response


def _list_accounts():
    """Return all Accounts."""
    return jsonify([_account_payload(account) for account in Account.all()]), 200


def _read_account(account_id):
    """Read one Account."""
    account = Account.find(account_id)
    if account is None:
        abort(404, description=f"Account with id [{account_id}] could not be found.")
    return jsonify(_account_payload(account)), 200


def _update_account(account_id):
    """Update an existing Account."""
    account = Account.find(account_id)
    if account is None:
        abort(404, description=f"Account with id [{account_id}] could not be found.")

    if request.content_type != "application/json":
        abort(415, description="Content-Type must be application/json")

    payload = request.get_json(silent=True) or {}
    merged = account.serialize()
    merged.update(payload)
    try:
        account.deserialize(merged)
    except DataValidationError as error:
        abort(400, description=str(error))

    duplicate = Account.query.filter(Account.email == account.email, Account.id != account.id).first()
    if duplicate:
        db.session.rollback()
        abort(409, description="Account with that email already exists")

    account.update()
    return jsonify(_account_payload(account)), 200


def _delete_account(account_id):
    """Delete an Account. DELETE is idempotent for this service."""
    account = Account.find(account_id)
    if account is not None:
        account.delete()
    return "", 204


def register_routes(app):
    """Register API endpoints on the Flask application."""

    @app.get("/")
    def index():
        return jsonify(name="Account REST API Service", version="1.0"), 200

    @app.get("/health")
    def health():
        return jsonify(status="OK"), 200

    # The IBM lab uses /accounts. The /api/accounts aliases are retained for
    # backwards compatibility with the original version of this repository.
    app.add_url_rule("/accounts", "create_accounts", _create_account, methods=["POST"])
    app.add_url_rule("/accounts", "list_accounts", _list_accounts, methods=["GET"])
    app.add_url_rule("/accounts/<int:account_id>", "get_account", _read_account, methods=["GET"])
    app.add_url_rule("/accounts/<int:account_id>", "update_account", _update_account, methods=["PUT"])
    app.add_url_rule("/accounts/<int:account_id>", "delete_account", _delete_account, methods=["DELETE"])

    app.add_url_rule("/api/accounts", "api_create_accounts", _create_account, methods=["POST"])
    app.add_url_rule("/api/accounts", "api_list_accounts", _list_accounts, methods=["GET"])
    app.add_url_rule("/api/accounts/<int:account_id>", "api_get_account", _read_account, methods=["GET"])
    app.add_url_rule("/api/accounts/<int:account_id>", "api_update_account", _update_account, methods=["PUT"])
    app.add_url_rule("/api/accounts/<int:account_id>", "api_delete_account", _delete_account, methods=["DELETE"])
