from flask import render_template, request
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm

@app.route("/")
def index():
    # Pobieranie wszystkich opublikowanych wpisów
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_posts=all_posts)

# Wspólna funkcja dla tworzenia i edycji wpisów
def save_entry(entry=None):
    form = EntryForm(obj=entry)
    errors = None
    
    if request.method == 'POST':
        if form.validate_on_submit():
            if entry is None:  # Tworzenie nowego wpisu
                entry = Entry()
                db.session.add(entry)
            
            form.populate_obj(entry)
            db.session.commit()
            return redirect(url_for('homepage'))  # Powrót na stronę główną po zapisie
        
        else:
            errors = form.errors
    
    return render_template("entry_form.html", form=form, errors=errors)

# Funkcja obsługująca tworzenie nowego wpisu
@app.route("/new-post/", methods=["GET", "POST"])
def create_entry():
    return save_entry()

# Funkcja obsługująca edycję wpisu
@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    return save_entry(entry)

