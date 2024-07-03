#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Plant(db.Model, SerializerMixin):
    __tablename__ = 'plants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    image = db.Column(db.String)
    price = db.Column(db.Float)
    is_in_stock = db.Column(db.Boolean)

    def __repr__(self):
        return f'<Plant {self.name} | In Stock: {self.is_in_stock}>'

@app.route('/plants/<int:id>', methods=['PATCH'])
def update_plant(id):
    plant = Plant.query.get_or_404(id)

    data = request.get_json()
    if 'is_in_stock' in data:
        plant.is_in_stock = data['is_in_stock']

    db.session.commit()

    return make_response(jsonify(plant.to_dict()), 200)

@app.route('/plants/<int:id>', methods=['DELETE'])
def delete_plant(id):
    plant = Plant.query.get_or_404(id)

    db.session.delete(plant)
    db.session.commit()

    return '', 204  

if __name__ == '__main__':
    app.run(port=5555, debug=True)
