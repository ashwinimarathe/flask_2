import logging


from flask import Flask, session, render_template, request, url_for, redirect, flash

app = Flask(__name__)

users = {
    'ashwini':{
                'books': [],
                'rentedbooks': []

            },
    'dhruv':{
                'books': [{
                    'title': 'Harry Potter 2',
                    'author': 'J.K.Rowling',
                    'publisher': 'piblisher 1',
                    'publishyear': '1998',
                    'id': 'Harry Potter 2'}
                ]
    }

}

books = {}

# @app.route('/')
# def hello():
#     """Return a friendly HTTP greeting."""
#     return 'Hello World!'


@app.route('/newroute/<name>')
def newroute(name):
    """parameter"""
    return "this was passed in: %s" % name


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

@app.route('/')
def index():
    #user_id = session.get('user_id')
    user_id = "ashwini"
    books = users[user_id]['books']
    rentedbooks = users[user_id]['rentedbooks']
    print(books)
    return render_template('index.html', books=books, rentedbooks = rentedbooks)


@app.route('/create', methods=('GET', 'POST'))
def create():
    new_book = {}
    user_id = "ashwini"
    if request.method == 'POST':
        new_book['title'] = request.form['title']
        new_book['author'] = request.form['author']
        new_book['publisher'] = request.form['publisher']
        new_book['publishyear'] = request.form['publishyear']
        new_book['id'] = (new_book['title'].replace(" ",""))+"_"+user_id
        error = None

        if not new_book['title']:
            error = 'Title is required.'
        if not new_book['author']:
            error = 'Author is required.'

        if error is not None:
            flash(error)
        else:
            user_id = "ashwini"
            users[user_id]['books'].append(new_book)
            
        return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/findbook', methods=('GET', 'POST'))
def findbook():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        if title is not None:
            print("Test")
        print(f"title {title}")
        user_id = "ashwini"
        if title is not None:
            return redirect(url_for('rent', title=title))
        elif author is not None:
            return redirect(url_for('rent', title=author)) 

        return redirect(url_for('rent', title=title))
    # GET request
    return render_template('find.html')


@app.route('/rent/<title>', methods=('GET', 'POST'))
def rent(title):
    rentablebooks = []
    if request.method == 'GET':
        #user_id = session.get('user_id')
        user_id = "ashwini"
        for user in users:
            book_list = users[user_id]['books']
            for book in book_list:
                print(f"user {user} book {book}")
                if book['title'] == title:
                    rentablebooks.append(book)
         
        return render_template('rent.html', books=rentablebooks)
    elif request.method == 'POST':
        bookid = request.form['submit_button']
        print("debug: bookid: "+bookid)
        #user_id = session.get('user_id')
        user_id = "ashwini"
        ownerid = bookid.split("_")[1]
        rented_book = None
        for user in users:
            for book in user['books']:
                if book['id'] == bookid:
                    rented_book = book
                    break

        users[user_id]['books'].append(rented_book)
        return redirect(url_for('index.html'))


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)