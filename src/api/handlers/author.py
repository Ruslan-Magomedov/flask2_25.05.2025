from api import db, app
from flask import request, abort, jsonify
from api.models.author import AuthorModel
from api.models.quote import QuoteModel


@app.get("/authors")
def get_authors():
    try:
        query = db.session.scalars(db.select(AuthorModel)).all()
    except Exception as e:
        abort(503, f"Database error: {str(e)}")
    authors_temp = [author.to_dict() for author in query]
    return authors_temp, 200


@app.get("/authors/<int:author_id>")
def get_author_byid(author_id: int):
    query = db.get_or_404(entity=AuthorModel, ident=author_id)
    return query.to_dict(), 200


@app.post("/authors")
def create_author():
    author_data = request.json
    # add_to_db(AuthorModel, author_data)  # Variant 2
    try:
        author = AuthorModel(**author_data)
        db.session.add(author)
        db.session.commit()
    except TypeError:
        abort(400, f"Invalid data. Required: <name>. Received: {', '.join(author_data.keys())}")
    except Exception as e:
        abort(503, f"Database error: {str(e)}")
    return jsonify(author.to_dict()), 201


@app.put("/authors/<int:author_id>")
def change_author_byid(author_id: int):
    new_data = request.json
    result = check(new_data)

    if not result[0]:
        return abort(400, result[1].get('error'))
        
    query = db.get_or_404(entity=AuthorModel, ident=author_id)
    return query.to_dict(), 200


# URL: "/authors/<int:author_id>/quotes"
@app.route("/authors/<int:author_id>/quotes", methods=["GET", "POST"])
def author_quotes(author_id: int):
    author = db.get_or_404(AuthorModel, author_id, description=f"Author with id={author_id} not found")

    if request.method == "GET":
        quotes = [quote.to_dict() for quote in author.quotes]
        return jsonify({"author": author.name} | {"quotes": quotes}), 200

    elif request.method == "POST":
        data = request.json
        new_quote = QuoteModel(author, **data)
        db.session.add(new_quote)
        db.session.commit()
        return jsonify(new_quote.to_dict() | { "author_id" : author.id}), 201
    else:
        abort(405)

