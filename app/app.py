from flask import Flask, redirect, render_template, request, url_for
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.mongoengine import MongoEngine
from flask.ext.mongoengine.wtf import model_form
from wtforms import validators

app = Flask(__name__)
app.debug = True
app.config['MONGODB_SETTINGS'] = {
    'db': 'flask-mongolab',
    'host': 'ds047305.mongolab.com',
    'port': 47305,
    'username': 'flask',
    'password': 'secret'
}
app.config['SECRET_KEY'] = '<replace with a secret key>'
app.config['DEBUG_TB_PANELS'] = ['flask.ext.mongoengine.panels.MongoDebugPanel']

db = MongoEngine(app)
toolbar = DebugToolbarExtension(app)


class User(db.Document):
    email = db.StringField(required=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)


class Post(db.Document):
    title = db.StringField(max_length=120, required=True,
                           validators=[validators.InputRequired(message=u'Missing title.'), ])
    author = db.ReferenceField(User)
    tags = db.ListField(db.StringField(max_length=30))
    content = db.StringField()


PostForm = model_form(Post)
UserForm = model_form(User)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/post/add', methods=['GET', 'POST'])
def post_add():
    form = PostForm(request.form)
    if request.method == 'POST' and form.validate():
        p = Post()
        form.populate_obj(p)
        p.save()
        return redirect(url_for('post_list'))
    return render_template('post/edit.html', form=form)


@app.route('/post/<id>')
def post_detail(id):
    return id


@app.route('/posts', methods=['GET'])
def post_list():
    posts = Post.objects

    return render_template('post/index.html', posts=posts)


@app.route('/user/add', methods=['GET', 'POST'])
def user_add():
    ross = User(email='ross@example.com', first_name='Ross', last_name='Lawley').save()
    return str(ross)


@app.route('/sample2')
def sample2():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
