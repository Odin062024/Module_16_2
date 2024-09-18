from flask import render_template, request, flash, redirect, url_for
from blog import app, db
from blog.models import Entry, User
from blog.forms import EntryForm, LoginForm
from functools import wraps
from flask_login import LoginManager, current_user, login_user, logout_user

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def login_required(view_func):
    @wraps(view_func)
    def check_permissions(*args, **kwargs):
        if current_user.is_authenticated:
            return view_func(*args, **kwargs)
        return redirect(url_for('login', next=request.path))
    return check_permissions

@app.route("/")
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_posts=all_posts)

def save_entry(entry=None):
    form = EntryForm(obj=entry)
    errors = None
    
    if request.method == 'POST':
        if form.validate_on_submit():
            if entry is None:
                entry = Entry()
                db.session.add(entry)
            
            form.populate_obj(entry)
            db.session.commit()
            return redirect(url_for('index'))
        
        else:
            errors = form.errors
    
    return render_template("entry_form.html", form=form, errors=errors)

@app.route("/new-post/", methods=["GET", "POST"])
@login_required
def create_entry():
    return save_entry()

@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
@login_required
def edit_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    return save_entry(entry)

@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    errors = None
    next_url = request.args.get('next')
    
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Jesteś teraz zalogowany.', 'success')
                return redirect(next_url or url_for('index'))
            else:
                flash('Niepoprawna nazwa użytkownika lub hasło.', 'error')
        else:
            errors = form.errors
    return render_template("login_form.html", form=form, errors=errors)

@app.route('/logout/', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Jesteś teraz wylogowany.', 'success')
    return redirect(url_for('index'))

@app.route("/delete-entry/<int:entry_id>", methods=['POST'])
@login_required
def delete_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    flash('Wpis został usunięty.', 'success')
    return redirect(url_for('list_drafts'))

@app.route("/drafts/", methods=['GET'])
@login_required
def list_drafts():
   drafts = Entry.query.filter_by(is_published=False).order_by(Entry.pub_date.desc())
   return render_template("drafts.html", drafts=drafts)

