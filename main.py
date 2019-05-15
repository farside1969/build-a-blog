from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:LaunchCode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'f8wv3w2f>v9j4sEuhcNYydAGMzzZJgkGgyHE9gUqaJcCk^f*^o7fQyBT%XtTvcYM'

#store post
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.String(750))

    def __init__(self, title, body ):
        self.title = title
        self.body = body

    #validate
    def is_valid(self):
        if self.title and self.body:
            return True
        else:
            return False

#display entry redirect
@app.route("/")
def index():
    return redirect("/blog")

#display entry handler
@app.route("/blog")
def display_blog_entries():
    #display single entry
    entry_id = request.args.get('id')
    if (entry_id):
        entry = Blog.query.get(entry_id)
        return render_template('single_entry.html', title="Blog Entry", entry=entry)

    else:
        all_entries = Blog.query.all()   
    return render_template('all_entries.html', title="All Entries", all_entries=all_entries)

#new entry
@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    if request.method == 'POST':
        new_entry_title = request.form['title']
        new_entry_body = request.form['body']
        new_entry = Blog(new_entry_title, new_entry_body)

        if new_entry.is_valid():
            db.session.add(new_entry)
            db.session.commit()

            # display recent blog entry
            url = "/blog?id=" + str(new_entry.id)
            return redirect(url)
#TODO - NEED TO FIX LOCATION OF ERRORS - USE USER-SIGNUP AS MODEL
        else:
            flash("Check entry for errors. Title and body are required.")
            return render_template('new_entry_form.html',
                title="Create new blog entry",
                new_entry_title=new_entry_title,
                new_entry_body=new_entry_body)
    #new entry form
    else:
        return render_template('new_entry_form.html', title="Create new blog entry")

if __name__ == '__main__':
    app.run()