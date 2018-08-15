from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret!'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ansible:ansible@localhost/'

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required(),
                                                         Length(1, 16)])
    submit = SubmitField('Submit')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), index=True, unique=True)

    def __repr__(self):
        return '<User {0}>'.format(self.name)

@app.route('/database')
def postgres():
    return redirect("http://localhost")


@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    new = False
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        if User.query.filter_by(name=name).first() is None:
            db.session.add(User(name=name))
            db.session.commit()
            new = True
    return render_template('index.html', form=form, name=name, new=new)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
