from flask import redirect, session
from functools import wraps


CategoryID = {
    1 : 'Alcohol',
    2 : 'Annual Fee',
    3 : 'Apartment things',
    4 : 'Books',
    5 : 'Clothing',
    6 : 'Coffee',
    7 : 'Dog',
    8 : 'Donations',
    9 : 'Electronics',
    10 : 'Entertainment',
    11 : 'Flight, Travel',
    12 : 'Food (out)',
    13 : 'Gifts',
    14 : 'Groceries',
    15 : 'Gym',
    16 : 'Internet Services',
    17 : 'Medical',
    18 : 'Other',
    19 : 'Personal Hygiene & Health',
    20 : 'Rent',
    21 : 'Shopping',
    22 : 'Transportation',
    23 : 'Utilities'
}

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def usd(value):
    """Format value as USD."""
    value = float(value)
    return f"${value:,.2f}"