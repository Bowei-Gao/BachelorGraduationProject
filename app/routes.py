import os
import shutil
from flask import render_template, redirect, url_for, request, abort, flash, Flask, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from app import app, login, db
from app.forms import LoginForm, MyForm, RegistrationForm
from flask_login import logout_user, login_required, current_user, login_user
from app.models import User
from app.jmetal.main import jmatal
from app.cplex.e_constraint import e_constraint
from app.cplex.CWMOIP import CWMOIP
from app.cplex.optimize_interval import optimize_interval
from app.plot import plot

# app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.txt']
app.config['UPLOAD_PATH'] = 'app/uploads'


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route('/file_upload', methods=['GET', 'POST'])
@login_required
def file_upload():
    form = MyForm()
    if request.method == 'POST':
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(400)
            filename = 'nrp1.txt'
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        return redirect(url_for('index'))
    return render_template('file_upload.html', title='File Upload', form=form)


@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/run_nsga_ii')
@login_required
def run_nsga_ii():
    total_time, evenness, len_solutions, solutions = jmatal()
    plot(solutions)
    shutil.move("NRP_result.png", "app/static/NRP_result.png")
    return render_template('nsga_ii.html', title='NSGA-II', total_time=total_time, evenness=evenness,
                           len_solutions=len_solutions, solutions=solutions)


@app.route('/run_e_constraint')
@login_required
def run_e_constraint():
    total_time, evenness, len_solutions, solutions = e_constraint()
    plot(solutions)
    shutil.move("NRP_result.png", "app/static/NRP_result.png")
    return render_template('e_constraint.html', title='e-constraint', total_time=total_time, evenness=evenness,
                           len_solutions=len_solutions, solutions=solutions)


@app.route('/run_cwmoip')
@login_required
def run_cwmoip():
    total_time, evenness, len_solutions, solutions = CWMOIP()
    plot(solutions)
    shutil.move("NRP_result.png", "app/static/NRP_result.png")
    return render_template('cwmoip.html', title='cwmoip', total_time=total_time, evenness=evenness,
                           len_solutions=len_solutions, solutions=solutions)


@app.route('/run_optimize_interval')
@login_required
def run_optimize_interval():
    total_time, evenness, len_solutions, solutions = optimize_interval()
    plot(solutions)
    shutil.move("NRP_result.png", "app/static/NRP_result.png")
    return render_template('optimize_interval.html', title='optimize interval', total_time=total_time,
                           evenness=evenness, len_solutions=len_solutions, solutions=solutions)


