import json
from flask import Flask, request, jsonify, render_template
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, Contact

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)
Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)


@app.route('/')
def root():
    return render_template('index.html')


@app.route("/api/contacts", methods=['GET', 'POST'])
@app.route("/api/contacts/<int:id>", methods=['GET', 'PUT', 'DELETE'])
@app.route("/api/contacts/name/<name>", methods=['GET'])
def contacts(id = None, name = None):
    if request.method == 'GET':
        if name is not None:
            contact = Contact.query.filter_by(name="Luis Rodriguez").first()
            contacts = Contact.query.filter(Contact.name.like(""+name+"%")).all()
            print(contacts)
            #return jsonify(conacts), 200
        elif id is not None:
            contact = Contact.query.get(id)
            if contact:
                return jsonify(contact.serialize()), 200
            else:
                return jsonify({"msg": "Contact not found"}), 404
        else:
            contacts = Contact.query.all()
            contacts = list(map(lambda contact: contact.serialize(), contacts))
            return jsonify(contacts), 200


    if request.method == 'POST':
        name = request.json.get("name", None)
        phone = request.json.get("phone", None)

        if not name:
            return jsonify({"msg": "Name is required"}), 400
        if not phone:
            return jsonify({"msg": "Phone is required"}), 400

        contact = Contact()
        contact.name = name
        contact.phone = json.dumps(phone)
        contact.save()

        return jsonify(contact.serialize()), 201
        

    if request.method == 'PUT':
        name = request.json.get("name", None)
        phone = request.json.get("phone", None)

        if not name:
            return jsonify({"msg": "Name is required"}), 400
        if not phone:
            return jsonify({"msg": "Phone is required"}), 400

        contact = Contact.query.get(id)

        if not contact:
            return jsonify({"msg": "Contact not found"}), 404

        contact.name = name
        contact.phone = json.dumps(phone)
        contact.update()

        return jsonify(contact.serialize()), 200

    if request.method == 'DELETE':
        contact = Contact.query.get(id)

        if not contact:
            return jsonify({"msg": "Contact not found"}), 404

        contact.delete()

        return jsonify({"success": "Contact was deleted"}), 200


if __name__ == "__main__":
    manager.run()