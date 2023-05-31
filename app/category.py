from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
# Configuracion basica para la conecxion con la BBDD
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/bdpythonapi'
# Para que no este saliendo alertas
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)  # sirve para declarar los Schemas


# Creacion de tabla
class Category(db.Model):
    cat_id = db.Column(db.Integer, primary_key=True)
    cat_nom = db.Column(db.String(100))
    cat_desp = db.Column(db.String(100))

    def __init__(self, cat_nom, cat_desp):
        self.cat_nom = cat_nom
        self.cat_desp = cat_desp


# Creación de Schema
class CategorySchema(ma.Schema):
    class Meta:
        fields = ('cat_id', 'cat_nom', 'cat_desp')


with app.app_context():
    db.create_all()

# para una solo respuesta
category_schema = CategorySchema()

# para muchas respustas
categories_schema = CategorySchema(many=True)


# GET######################################
@app.route('/categories', methods=['GET'])
def get_categorias():
    all_categorias = Category.query.all()
    result = categories_schema.dump(all_categorias)
    return jsonify(result)


# GET by id################################
@app.route('/categories/<id>', methods=['GET'])
def get_category_by_id(id):
    category = Category.query.get(id)
    return category_schema.jsonify(category)


# POST######################################
@app.route('/categories', methods=['POST'])
def insert_category():
    data = request.get_json(force=True)
    cat_nom = data['cat_nom']
    cat_desp = data['cat_desp']

    category = Category(cat_nom, cat_desp)
    db.session.add(category)
    db.session.commit()

    return category_schema.jsonify(category)

# PUT#######################################
@app.route('/categories/<id>', methods=['PUT'])
def update_category(id):
    categoriaAtualizada = Category.query.get(id)
    data = request.get_json(force=True)
    cat_nom = data['cat_nom']
    cat_desp = data['cat_desp']

    categoriaAtualizada.cat_nom = cat_nom
    categoriaAtualizada.cat_desp = cat_desp

    db.session.commit()

    return category_schema.jsonify(categoriaAtualizada)

#DELETE#######################################
@app.route('/categories/<id>', methods=['DELETE'])
def delete_category(id):
    categoriaEliminar = Category.query.get(id)
    db.session.delete(categoriaEliminar)
    db.session.commit()

    return category_schema.jsonify(categoriaEliminar)

# Mensaje de Bienvenida
@app.route('/', methods=['GET'])
def index():
    return jsonify({'Mensaje': 'Bienvenido al tutorial de PYTHON'})


if __name__ == "__main__":
    app.run(debug=True)
