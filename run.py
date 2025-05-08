from app import create_app, db
from app.models import Product

app = create_app()

# Автоматическое создание таблиц и начальное заполнение при запуске
with app.app_context():
    db.create_all()

    # Добавляем примеры платьев, если каталог пуст
    if Product.query.count() == 0:
        sample_products = [
            Product(
                name='Классическое свадебное платье',
                price=45000.0,
                description='Белоснежное классическое платье с кружевным лифом и длинным шлейфом.',
                image='dress1.png'
            ),
            Product(
                name='Бохо-платье свадебное',
                price=38000.0,
                description='Воздушное платье в стиле бохо с вышивкой и открытыми плечами.',
                image='dress1.png'
            ),
            Product(
                name='Современное свадебное платье',
                price=52000.0,
                description='Современный силуэт, сочетание шелка и шифона, минималистичный дизайн.',
                image='dress1.png'
            ),
        ]
        db.session.bulk_save_objects(sample_products)
        db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
