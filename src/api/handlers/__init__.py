from flask import jsonify
from api import app
from werkzeug.exceptions import HTTPException


@app.errorhandler(HTTPException)
def handle_exception(e):
    """ Функция для перехвата HTTP ошибок и возврата в виде JSON."""
    return jsonify({"error": str(e)}), e.code


def check(data: dict, check_rating=False) -> tuple[bool, dict]:
    keys = ('author', 'text')
    if check_rating:
        rating = data.get('rating')    
        if rating and rating not in range(1, 6):
            return False, {"error": "Rating must be between 1 and 5"}
    
    if set(data.keys()) - set(keys):
        return False, {"error": "Invalid fields to create/update"}
    return True, data
