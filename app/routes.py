from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from .models import User, Employee
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Пользователь с таким именем уже существует')
            return redirect(url_for('main.register'))
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация прошла успешно! Теперь вы можете войти.')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Неправильное имя пользователя или пароль')
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@bp.route('/add_employee', methods=['GET', 'POST'])
@login_required
def add_employee():
    if request.method == 'POST':
        full_name = request.form['full_name']
        position = request.form['position']
        department = request.form['department']
        phone = request.form['phone']
        email = request.form['email']
        hire_date = datetime.strptime(request.form['hire_date'], '%Y-%m-%d').date()
        employee = Employee(full_name=full_name, position=position, department=department, phone=phone, email=email, hire_date=hire_date)
        db.session.add(employee)
        db.session.commit()
        flash('Сотрудник успешно добавлен!')
        return redirect(url_for('main.index'))
    return render_template('add_employee.html')

@bp.route('/edit_employee/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    if request.method == 'POST':
        employee.full_name = request.form['full_name']
        employee.position = request.form['position']
        employee.department = request.form['department']
        employee.phone = request.form['phone']
        employee.email = request.form['email']
        employee.hire_date = datetime.strptime(request.form['hire_date'], '%Y-%m-%d').date()
        db.session.commit()
        flash('Данные сотрудника обновлены!')
        return redirect(url_for('main.index'))
    return render_template('edit_employee.html', employee=employee)

@bp.route('/delete_employee/<int:id>')
@login_required
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    flash('Сотрудник удален!')
    return redirect(url_for('main.index'))
