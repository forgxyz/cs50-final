import json

from flask import redirect, session
from functools import wraps

with open('data/category_ids.json') as f:
    CategoryID = json.load(f)

def usd(value):
    """Format value as USD."""
    value = float(value)
    return f"${value:,.2f}"