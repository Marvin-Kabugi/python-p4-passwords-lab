#!/usr/bin/env python3

from flask import request, session, make_response, jsonify
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    
    def post(self):
        json = request.get_json()
        user = User(
            username=json.get('username'),
        )
        user.password_hash = json.get('password')
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201

class CheckSession(Resource):
    def get(self):
        session['user_id'] = session.get('user_id') or None
        
        if session['user_id']:
            user = User.query.filter_by(id=session['user_id']).first()
            if user:
                return user.to_dict(), 200
        
        return {'error': 'Unauthorized'}, 204
    
class Login(Resource):
    def post(self):
        username = request.get_json()['username']
        password = request.get_json()['password']
        print(username, password)

        user = User.query.filter_by(username=username).first()
        print(user)

        if user.authenticate(password):
            session['user_id'] = user.id
            return user.to_dict(), 200
        
        return {'error': 'Invalid username or password'}, 401

class Logout(Resource):
    def delete(self):
        session['user_id'] = None

        return {}, 204

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
