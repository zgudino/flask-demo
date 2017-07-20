from flask import Flask, jsonify
from flask import request
from flask_mongoengine import MongoEngine
from app.errors.invalid_usage import InvalidUsage

db = MongoEngine()

app = Flask(__name__)
app.config.from_object(__name__)

db.init_app(app)


@app.errorhandler(InvalidUsage)
def invalid_usage_handler(error):
    return jsonify(error.to_dict())


@app.route('/authors', methods=['POST', 'GET', 'DELETE', 'PUT'])
def authors():
    from app.models import Author
    try:
        if request.method == 'POST':
            author = Author(username=request.form['username'], email=request.form['email'], name=request.form['name'])
            author.save(validate=True)

            return jsonify(author.json)
        elif request.method == 'DELETE':
            if not request.form['id']:
                raise InvalidUsage('Error - Olvido el campo id', 500)

            Author.objects(pk=request.form['id']).delete()
            return jsonify(dict(status=200, message='Documento fue eliminado con exito.'))

        elif request.method == 'PUT':
            author = Author.objects(id=request.form['id']).get()
            new_author = dict(request.form)

            diff = {k: v for k, v in new_author.items() if author.__contains__(k) and author[k] != new_author[k]}

            for k, v in diff.items():
                sets = {'set__{0}'.format(k): v[0]}
                author.update(**sets)

            author.reload()
            return jsonify(author.json)
        else:
            return jsonify(dict(authors=[a.json for a in Author.objects]))
    except Exception as err:
        raise err.with_traceback(err.__traceback__)


@app.route('/books', methods=['GET', 'POST', 'DELETE'])
@app.route('/books/author/<string:author_username>', methods=['GET'])
def books(author_username=None):
    from app.models import Author, Book
    try:
        if request.method == 'POST':
            author_id = request.form['author_id'] or None

            if not author_id:
                raise InvalidUsage('Id de autor no fue encontrado.', status_code=503)

            book = Book(title=request.form['title'])
            book.author = Author.objects.get(pk=author_id)
            book.save()

            return jsonify(book.json)

        elif request.method == 'DELETE':
            if not request.form['book_id']:
                raise InvalidUsage('Olvido el campo book_id')

            Book.objects(pk=request.form['book_id']).delete()

            return jsonify(dict(status=200, message='Documento fue eliminado con exito.'))

        else:
            if author_username:
                return jsonify(
                    dict(author_books=[book.json for book in Book.objects(author=Author.objects.get(name=author_username))]))

            return jsonify(dict(books=[book.json for book in Book.objects]))
    except Exception as err:
        raise err.with_traceback(err.__traceback__)
