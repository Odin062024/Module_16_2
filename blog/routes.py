from flask import render_template
from blog import app
from blog.models import Entry

@app.route("/")
def index():
    # Pobieranie wszystkich opublikowanych wpisów, posortowanych malejąco według daty publikacji
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc()).all()
    
    # Renderowanie szablonu strony głównej i przekazanie wpisów
    return render_template("homepage.html", all_posts=all_posts)
