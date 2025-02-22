import os
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
import markdown2
import logging
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from flask_jwt_extended import JWTManager
from db_operations import DatabaseManager, settings
from datetime import timedelta
from main import generate_response
from generate_tables import create_tables

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = settings.JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=int(settings.TOKEN_EXPIRE_IN_DAYS))
jwt = JWTManager(app)

db_manager = DatabaseManager()
CORS(app)

@app.route('/signin', methods=['POST'])
def signin():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = db_manager.check_user(username)

    if user and user[-1] == password:
        additional_claims = {
            "user_id": user[0], 
            "user_name": user[2],
            "createdon": user[3]
        }
        access_token = create_access_token(username, additional_claims=additional_claims)
        return jsonify({'access_token': access_token}), 200

    return jsonify({"error": "Invalid credentials"}), 401


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    created_by = data.get("created_by", None)

    if not (first_name and last_name and username and email and password):
        return jsonify({"message": "Missing required fields"}), 400
    
    hashed_password = generate_password_hash(password)
    user = db_manager.create_user(first_name, last_name, username, email, hashed_password)    
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401

    return jsonify({"message": "User created successfully"}), 201


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        query = data.get('query', '').lower()
        user_id = data.get('user_id')
        email = db_manager.check_user(userid=user_id)
        if user_id and email:
            email = email.Email
            if query.lower() == 'quit':
                return jsonify({"error": "Session ended"}), 400

            context = generate_response(query)
            
            full_context = f"\n\n{context}"
            answer = full_context

            formatted_answer = markdown2.markdown(answer, extras=["tables"])
            return jsonify({"answer":formatted_answer}), 200
        return jsonify({"msg":"Invalid User"})
    except Exception as e:
        logging.error(f"Error processing query: {str(e)}")
        return jsonify({"error": f"An error occurred : {e}"}), 500


@app.route('/token_details', methods=['GET'])
@jwt_required()
def get_token_details():
    claims = get_jwt()
    response = {
        "user_id": claims.get('user_id'),
        "email": claims.get('sub'),
        "username": claims.get('user_name')
    }
    return jsonify({"message": response}), 200


@app.route('/chat_history', methods=['GET'])
@jwt_required()
def get_chat_history():
    claims = get_jwt()
    user_id = claims.get('user_id', 'anonymous')
    history = db_manager.get_chat_history(user_id)
    return jsonify({"history": history}), 200


@app.route('/top_faqs', methods=['GET'])
@jwt_required()
def get_top_faqs():
    claims = get_jwt()
    user_id = claims.get('user_id', 'anonymous')
    top_faqs = db_manager.get_top_faqs(user_id)
    return jsonify({"top_faqs": top_faqs}), 200


@app.route('/userprofile_list', methods=['GET'])
@jwt_required()
def get_userprofile_list():
    data = db_manager.get_userprofile_list()
    return jsonify({"data": data}), 200

# app.register_blueprint(api)
if __name__ == "__main__":
        app.run(port=5005, debug=True, use_reloader=True)
        # app.run(host='192.168.27.200', port=5005, debug=True, use_reloader=True)
    