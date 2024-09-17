from flask import render_template, request, redirect, url_for
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm

@app.route("/")
def index():
    # Pobieranie wszystkich opublikowanych wpisów, posortowanych malejąco według daty publikacji
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc()).all()
    
    # Renderowanie szablonu strony głównej i przekazanie wpisów
    return render_template("homepage.html", all_posts=all_posts)

@app.route("/new-post/", methods=["GET", "POST"])
def create_entry():
    form = EntryForm()
    errors = None
    if request.method == 'POST':
        if form.validate_on_submit():
            entry = Entry(
                title=form.title.data,
                body=form.body.data,
                is_published=form.is_published.data
            )
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            errors = form.errors
    return render_template("entry_form.html", form=form, errors=errors)
