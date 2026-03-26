from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель для игр
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'Game: {self.name} ({self.year})'

@app.route('/')
def index():
    games = Game.query.all()
    return render_template('index.html', games=games)

@app.route('/add', methods=['POST'])
def add_game():
    name = request.form.get('name')
    year = request.form.get('year')
    
    if name and year:
        new_game = Game(name=name, year=int(year))
        db.session.add(new_game)
        db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/delete/<int:game_id>', methods=['POST'])
def delete_game(game_id):
    game = Game.query.get_or_404(game_id)
    db.session.delete(game)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("База данных создана!")
        print("Добавьте игры через форму на главной странице")
    app.run(debug=True)