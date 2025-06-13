from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://root:{os.getenv('DB_PASSWORD')}@localhost/crud_tarefas"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app, version='1.0', title='Task CRUD API',
          description='Uma API simples de tarefas com Flask + MySQL + Swagger')

ns = api.namespace('Tarefas', description='Operações com tarefas')

class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    prazo = db.Column(db.String(10))
    status = db.Column(db.String(20), default='pendente')

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "prazo": self.prazo,
            "status": self.status
        }

tarefa_model = api.model('Tarefa', {
    'id': fields.Integer(readonly=True),
    'titulo': fields.String(required=True, description='Título da tarefa'),
    'descricao': fields.String(description='Descrição da tarefa'),
    'prazo': fields.String(description='Prazo (AAAA-MM-DD)'),
    'status': fields.String(description='Status da tarefa', default='pendente')
})

@ns.route('/')
class ListaTarefas(Resource):
    @ns.marshal_list_with(tarefa_model)
    def get(self):
        return Tarefa.query.all()

    @ns.expect(tarefa_model)
    @ns.marshal_with(tarefa_model, code=201)
    def post(self):
        dados = api.payload
        nova = Tarefa(
            titulo=dados['titulo'],
            descricao=dados.get('descricao', ''),
            prazo=dados.get('prazo', ''),
            status=dados.get('status', 'pendente')
        )
        db.session.add(nova)
        db.session.commit()
        return nova, 201

@ns.route('/<int:id>')
@ns.response(404, 'Tarefa não encontrada')
@ns.param('id', 'ID da tarefa')
class TarefaResource(Resource):
    @ns.marshal_with(tarefa_model)
    def get(self, id):
        tarefa = Tarefa.query.get_or_404(id)
        return tarefa

    @ns.expect(tarefa_model)
    @ns.marshal_with(tarefa_model)
    def put(self, id):
        tarefa = Tarefa.query.get_or_404(id)
        dados = api.payload
        tarefa.titulo = dados.get('titulo', tarefa.titulo)
        tarefa.descricao = dados.get('descricao', tarefa.descricao)
        tarefa.prazo = dados.get('prazo', tarefa.prazo)
        tarefa.status = dados.get('status', tarefa.status)
        db.session.commit()
        return tarefa

    @ns.response(200, 'Tarefa deletada com sucesso')
    def delete(self, id):
        tarefa = Tarefa.query.get_or_404(id)
        db.session.delete(tarefa)
        db.session.commit()
        return {'mensagem': 'Tarefa deletada com sucesso'}, 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
