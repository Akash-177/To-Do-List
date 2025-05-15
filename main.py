from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

# Base directory for the database
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    contact = db.Column(db.String(100), unique=True)

    def __init__(self, name, contact):
        self.name = name
        self.contact = contact

# User schema
class UserSchema(ma.Schema):
    class Meta:  # Use 'Meta' instead of 'meta'
        fields = ('id', 'name', 'contact')

user_schema = UserSchema()
users_schema = UserSchema(many=True)  # Use many=True for a list of users

@app.route('/user',methods=['POST'])
def add_user():
    name=request.json['name']
    contact=request.json['contact']
    new_user=User(name,contact)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)

@app.route('/user', methods=['GET'])
def getAllUser():
    all_users = User.query.all()
    result=users_schema.dump(all_users)
    return jsonify(result)

@app.route('/user/<id>', methods=['GET'])
def getuserbyid(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

@app.route('/user/<id>', methods=['PUT'])
def updateuser(id):
    user = User.query.get(id)
    name=request.json['name']
    contact=request.json['contact']
    user.name = name
    user.contact = contact
    db.session.commit()
    return user_schema.jsonify(user)

@app.route('/user/<id>', methods=['DELETE'])
def deleteuser(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)



'''@app.route('/', methods=['GET'])
def home():
    return jsonify({'msg': 'Hellooooooooooo', 'name': 'Akash'})
'''

if __name__ == '__main__':
    with app.app_context():  # Create all tables if they don't exist
        db.create_all()
    app.run(debug=True)
