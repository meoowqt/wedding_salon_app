from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from . import db
from .models import User, Product, CartItem, Appointment
from .forms import LoginForm, RegistrationForm, AppointmentForm, ProductForm
from datetime import datetime

bp = Blueprint('app', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user or not check_password_hash(user.password_hash, form.password.data):
            flash('Неправильный email или пароль', 'danger')
            return redirect(url_for('app.login'))
        login_user(user)
        return redirect(url_for('app.index'))
    return render_template('login.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('app.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('app.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            is_admin=False
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Регистрация прошла успешно. Войдите в свой аккаунт.', 'success')
        return redirect(url_for('app.login'))
    return render_template('register.html', form=form)

@bp.route('/catalog')
def catalog():
    products = Product.query.all()
    return render_template('catalog.html', products=products)

@bp.route('/product/<int:id>', methods=['GET', 'POST'])
def product(id):
    p = Product.query.get_or_404(id)
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('Пожалуйста, войдите, чтобы добавить в корзину.', 'warning')
            return redirect(url_for('app.login'))
        item = CartItem.query.filter_by(user_id=current_user.id, product_id=p.id).first()
        if item:
            item.quantity += 1
        else:
            item = CartItem(user_id=current_user.id, product_id=p.id, quantity=1)
            db.session.add(item)
        db.session.commit()
        flash('Платье добавлено в корзину', 'success')
        return redirect(url_for('app.cart')) 
    return render_template('product.html', product=p)

@bp.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    if request.method == 'POST':
        date_str = request.form.get('date')
        cart_item_id = request.form.get('cart_item_id')

        if not cart_item_id or not date_str:
            flash('Выберите элемент корзины и дату', 'danger')
            return redirect(url_for('app.cart'))

        try:
            parsed_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            cart_item = CartItem.query.get(cart_item_id)

            if not cart_item or cart_item.user_id != current_user.id:
                flash('Ошибка элемента корзины', 'danger')
                return redirect(url_for('app.cart'))

            # Создаем запись на примерку
            appointment = Appointment(cart_item_id=cart_item.id, date=parsed_date)
            db.session.add(appointment)

            # Удаляем ВСЕ товары из корзины пользователя
            db.session.delete(cart_item)  # Удаляем только текущий элемент корзины
            
            db.session.commit()
            flash('✅ Запись на примерку успешна! Корзина очищена.', 'success')
            return redirect(url_for('app.cart'))

        except ValueError:
            flash('❌ Неверный формат даты (используйте YYYY-MM-DD)', 'danger')
            return redirect(url_for('app.cart'))
        except Exception as e:
            db.session.rollback()
            flash('❌ Ошибка при записи', 'danger')
            return redirect(url_for('app.cart'))

    # GET-запрос: отображаем корзину
    cart_items = current_user.cart_items
    return render_template('cart.html', cart_items=cart_items)



@bp.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.is_admin:
        flash('Доступ запрещён', 'warning')
        return redirect(url_for('app.index'))
    form = ProductForm()
    if form.validate_on_submit():
        prod = Product(
            name=form.name.data,
            price=form.price.data,
            description=form.description.data,
            image=form.image.data.filename
        )
        image_file = form.image.data
        image_file.save(f"{current_app.root_path}/static/uploads/{prod.image}")
        db.session.add(prod)
        db.session.commit()
        flash('Товар добавлен', 'success')
    products = Product.query.all()
    return render_template('admin.html', products=products, form=form)
