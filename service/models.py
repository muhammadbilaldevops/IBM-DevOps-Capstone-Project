"""Database model for Customer Accounts."""

from datetime import date

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class DataValidationError(ValueError):
    """Raised when an Account payload is missing required data."""


class Account(db.Model):
    """Customer Account persisted by the REST service."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(256), nullable=False)
    phone_number = db.Column(db.String(32), nullable=True)
    date_joined = db.Column(db.Date, nullable=False, default=date.today)

    def __repr__(self):
        return f"<Account {self.name} id=[{self.id}]>"

    def serialize(self):
        """Serialize the model into the JSON representation used by the API."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "phone_number": self.phone_number,
            "date_joined": self.date_joined.isoformat(),
        }

    def deserialize(self, data):
        """Load and validate an Account from a JSON dictionary."""
        if not isinstance(data, dict):
            raise DataValidationError("Invalid Account: body of request contained bad or no data")

        required = ("name", "email", "address")
        missing = [field for field in required if not data.get(field)]
        if missing:
            raise DataValidationError(f"Invalid Account: missing {missing[0]}")

        self.name = data["name"]
        self.email = data["email"]
        self.address = data["address"]
        self.phone_number = data.get("phone_number")

        joined = data.get("date_joined")
        if joined:
            try:
                self.date_joined = date.fromisoformat(joined)
            except (TypeError, ValueError) as error:
                raise DataValidationError("Invalid Account: date_joined must be YYYY-MM-DD") from error
        elif self.date_joined is None:
            self.date_joined = date.today()

        return self

    def create(self):
        """Persist this Account."""
        self.id = None
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Persist changes to this Account."""
        db.session.commit()

    def delete(self):
        """Delete this Account."""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def all(cls):
        """Return all Accounts ordered by id."""
        return cls.query.order_by(cls.id).all()

    @classmethod
    def find(cls, account_id):
        """Find an Account by primary key."""
        return db.session.get(cls, account_id)

    @classmethod
    def find_by_email(cls, email):
        """Find an Account by email address."""
        return cls.query.filter_by(email=email).first()
