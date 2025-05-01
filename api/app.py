# api/routes.py

from flask import Blueprint, jsonify, request, abort
from flask_restful import Api, Resource
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from app.database import Proyecto, User, Mensaje,db
from api.engine import engine

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

def obtener_usuarios():
    conn = get_db_connection()
    usuarios = conn.execute(text('SELECT id, nombre, fecha_registro, contrasenya FROM user_account')).fetchall()
    return [{'id': u[0], 'nombre': u[1], 'fecha_registro': u[2], 'contrasenya': u[3]} for u in usuarios]

def crear_usuario(nombre, contrasenya):
    user = User(nombre=nombre, contrasenya=contrasenya)
    conn = get_db_connection()
    conn.add(user)
    conn.commit()
    return user

def eliminar_usuario(user_id):
    conn = get_db_connection()
    user = User.query.get(user_id)
    if not user:
        return None
    user = conn.merge(user)
    conn.delete(user)
    conn.commit()
    return True

def get_db_connection():
    return db.session

class Usuarios(Resource):
    def get(self):
        return jsonify(obtener_usuarios())

    def post(self):
        data = request.get_json()
        nombre = data.get('nombre')
        contrasenya = data.get('contrasenya')

        if not nombre or not contrasenya:
            abort(400, description="Nombre y contraseña requeridos")

        crear_usuario(nombre, contrasenya)
        return {'message': 'Usuario creado'}, 201

    def delete(self):
        data = request.get_json()
        user_id = data.get('id')
        if not user_id:
            abort(400, description="ID requerido")

        resultado = eliminar_usuario(user_id)
        if not resultado:
            abort(404, description="Usuario no encontrado")

        return {'message': 'Usuario eliminado'}, 200

# Proyectos se queda igual por ahora
class Proyectos(Resource):
    def get(self):
        conn= get_db_connection()
        proyectos = conn.execute(text('SELECT id, nombre, descripcion, creador_id FROM proyecto')).fetchall()
        proyectos_dict = [{'id': p[0], 'nombre': p[1], 'descripcion': p[2], 'creador_id': p[3]} for p in proyectos]
        return jsonify(proyectos_dict)
    
    def post(self):
        data = request.get_json()
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        creador_id = data.get('creador_id')

        if not nombre or not creador_id:
            abort(400, description="Nombre y creador_id requeridos")

        proyecto=Proyecto(nombre=nombre, descripcion=descripcion, creador_id=creador_id)

        conn= get_db_connection()
        conn.add(proyecto)
        conn.commit()
        return {'message': 'Proyecto creado'}, 201
    
    def delete(self):
        proyecto_id = request.args.get('id')
        if not proyecto_id:
            abort(400, description="ID requerido")

        conn=get_db_connection
        proyecto = Proyecto.query.get(proyecto_id)
        if not proyecto:
            abort(404, description="Proyecto no encontrado")

        proyecto = conn.merge(proyecto)
        conn.delete(proyecto)
        conn.commit()

        return {'message': 'Proyecto eliminado'}, 200

class Mensajes(Resource):
    def get(self):
        conn=get_db_connection
        mensajes = conn.execute(text('SELECT id, mensaje, fecha_envio, usuario_id FROM mensajes')).fetchall()
        mensajes_dict = [{'id': m[0], 'mensaje': m[1], 'fecha_envio': m[2], 'usuario_id': m[3]} for m in mensajes]
        return jsonify(mensajes_dict)

    def post(self):
        data = request.get_json()
        print(data)
        mensaje = data.get('mensaje')
        usuario_id = data.get('usuario_id')
        proyecto_id = data.get('proyecto_id')

        if not mensaje or not usuario_id or not proyecto_id:
            abort(400, description="Mensaje y usuario_id requeridos")

        mensaje=Mensaje(contenido=mensaje, usuario_id=usuario_id,proyecto_id=proyecto_id)

        conn=get_db_connection()
        conn.add(mensaje)
        conn.commit()
        return {'message': 'Mensaje creado'}, 201

api.add_resource(Usuarios, '/usuarios')
api.add_resource(Proyectos, '/proyectos')
api.add_resource(Mensajes, '/mensajes')
