#!/usr/bin/env python3

from flask import Flask, jsonify, request, abort
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# Routes for Heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_data = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
    return jsonify(hero_data)

@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_hero(hero_id):
    hero = Hero.query.get(hero_id)
    if hero:
        powers = [{'id': power.id, 'name': power.name, 'description': power.description} for power in hero.powers]
        hero_data = {'id': hero.id, 'name': hero.name, 'super_name': hero.super_name, 'powers': powers}
        return jsonify(hero_data)
    else:
        return make_response(jsonify({'error': 'Hero not found'}), 404)

# Routes for Powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_data = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    return jsonify(power_data)

@app.route('/powers/<int:power_id>', methods=['GET', 'PATCH'])
def get_or_update_power(power_id):
    power = Power.query.get(power_id)
    if request.method == 'GET':
        if power:
            return jsonify({'id': power.id, 'name': power.name, 'description': power.description})
        else:
            return make_response(jsonify({'error': 'Power not found'}), 404)
    elif request.method == 'PATCH':
        if power:
            try:
                data = request.get_json()
                power.description = data.get('description', power.description)
                db.session.commit()
                return jsonify({'id': power.id, 'name': power.name, 'description': power.description})
            except ValueError:
                return make_response(jsonify({'errors': ['Validation errors']}), 400)
        else:
            return make_response(jsonify({'error': 'Power not found'}), 404)

# Route for creating HeroPower
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    try:
        data = request.get_json()
        strength = data.get('strength')
        power_id = data.get('power_id')
        hero_id = data.get('hero_id')

        hero_power = HeroPower(strength=strength, power_id=power_id, hero_id=hero_id)
        db.session.add(hero_power)
        db.session.commit()

        hero = Hero.query.get(hero_id)
        powers = [{'id': power.id, 'name': power.name, 'description': power.description} for power in hero.powers]
        hero_data = {'id': hero.id, 'name': hero.name, 'super_name': hero.super_name, 'powers': powers}
        return jsonify(hero_data)
    except ValueError:
        return make_response(jsonify({'errors': ['Validation errors']}), 400)

if __name__ == '__main__':
    app.run(port=5555)
