from flask import Flask,render_template,request,jsonify,session, flash,redirect, url_for
from list_data import *
import os
from models.my_en_convert import myan
from models.pali_my_convert import parli
import asyncio
from pymongo import MongoClient
import hashlib
import uuid
from datetime import datetime, timedelta
from functools import wraps
import requests
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017/")
db = client["comment_system"]
comments_collection = db["comments"]
users_collection = db["users"]

POST_ID = "namecheckerapp"


# active link
@app.context_processor
def inject_request():
    return dict(request=request)

@app.route('/')
def dashboard():
    weeks_loaded = int(request.args.get('weeks_loaded', 1))
    comments = get_comments_tree(weeks_loaded=weeks_loaded)
    return render_template(
        'dashboard.html',
        comments=comments,
        weeks_loaded=weeks_loaded,
        user=session.get('user')
    )

# use modal
@app.route('/convert_my',methods=['POST'])
def convert_my():
    data=request.get_json()
    name=data.get("name")    
    # code put
    if not name:
        return jsonify({"error": "Name is required!"}), 400

    # result=asyncio.run(myan(name))
    loop=asyncio.new_event_loop()
    result=loop.run_until_complete(myan(name))
    loop.close()
    return jsonify({"message": result})

# use modal
@app.route('/convert_parlit',methods=['POST'])
def convert_parlit():
    data=request.get_json()
    name=data.get("name")    
    # code put
    if not name:
        return jsonify({"error": "Name is required!"}), 400

    # result=asyncio.run(parli(name))
    loop=asyncio.new_event_loop()
    result=loop.run_until_complete(parli(name))
    loop.close()
    return jsonify({"message": result})


# about
@app.route('/about')
def about():
    return render_template('about.html')

# my-en
@app.route('/my_en')
def my_en():
    return render_template('my_en.html', **globals())

# parli
@app.route('/parli_en')
def parli_en():    
    return render_template('parli_en.html', **globals())

#comment function

# Helper Functions
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrap

def create_user(username, password):
    if users_collection.find_one({"username": username}):
        return False
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    users_collection.insert_one({
        "username": username,
        "password": hashed_pw,
        "created_at": datetime.utcnow()
    })
    return True

def authenticate(username, password):
    user = users_collection.find_one({"username": username})
    if user and user["password"] == hashlib.sha256(password.encode()).hexdigest():
        return True
    return False

@app.route('/comment')
def home():
    weeks_loaded = int(request.args.get('weeks_loaded', 1))
    comments = get_comments_tree(weeks_loaded=weeks_loaded)
    return url_for('dashboard')


def is_valid_gmail(email):
    pattern=r"^[a-zA-Z0-9.+-]+@gmail\.com$"
    return re.match(pattern,email)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_pw = request.form['confirm_pw']

        if password != confirm_pw:
            flash("Passwords do not match.")
        elif not is_valid_gmail(username):
            flash("User name must be email or gmail.")
        elif create_user(username, password):
            flash("Account created successfully! Please log in.")
            return redirect(url_for('login'))
        else:
            flash("Username already exists.")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate(username, password):
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('dashboard'))

@app.route('/add_comment', methods=['POST'])
@login_required
def add_comment():
    text = request.form['comment_text']
    if text.strip():
        comment_data = {
            "_id": uuid.uuid4().hex,
            "userId": session['user'],
            "postId": POST_ID,
            "text": text,
            "parentId": None,
            "likes": 0,
            "unlikes": 0,
            "createdAt": datetime.utcnow()
        }
        comments_collection.insert_one(comment_data)
    return redirect(url_for('dashboard'))

@app.route('/reply/<parent_id>', methods=['POST'])
@login_required
def reply_comment(parent_id):
    text = request.form['reply_text']
    if text.strip():
        reply_data = {
            "_id": uuid.uuid4().hex,
            "userId": session['user'],
            "postId": POST_ID,
            "text": text,
            "parentId": parent_id,
            "likes": 0,
            "unlikes": 0,
            "createdAt": datetime.utcnow()
        }
        comments_collection.insert_one(reply_data)
    return redirect(url_for('dashboard'))

@app.route('/like/<comment_id>')
@login_required
def like_comment(comment_id):
    comments_collection.update_one(
        {"_id": comment_id},
        {"$inc": {"likes": 1}}
    )
    return redirect(url_for('dashboard'))

@app.route('/unlike/<comment_id>')
@login_required
def unlike_comment(comment_id):
    comments_collection.update_one(
        {"_id": comment_id},
        {"$inc": {"unlikes": 1}}
    )
    return redirect(url_for('dashboard'))

def get_comments_tree(parent_id=None, weeks_loaded=1):
    start_date = datetime.utcnow()
    end_date = start_date - timedelta(days=weeks_loaded * 7)
    print(end_date)
    query = {
        # "postId": POST_ID,
        "parentId": parent_id,
        "createdAt": {"$gte": end_date}
    }
    
    session['start_date'] = start_date
    session['end_date'] = end_date
    comments = list(comments_collection.find(query).sort("createdAt", 1))
    for comment in comments:
        comment['replies'] = get_comments_tree(comment["_id"], weeks_loaded)
    return comments

#api call endpoint login,register,myanmar_to_english,pali_to_roman

baseURL = "http://localhost:8000"

@app.route('/api')
def api():
    return render_template('api_login.html',**globals())

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    # FastAPI ရဲ့ /token ကို form data ပုံစံနဲ့ပို့
    payload = {
        'grant_type': 'password',
        'username': username,
        'password': password,
        'scope': '',
        'client_id': 'string',
        'client_secret': 'string'
    }

    response = requests.post(
        f"{baseURL}/token",
        data=payload,
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401
    
@app.route('/api_register')
def api_register():
    return render_template('api_register.html', **globals())


@app.route('/api/register', methods=['POST'])
def api_register_func():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    # FastAPI ရဲ့ /token ကို form data ပုံစံနဲ့ပို့
    payload = {
        'username': username,
        'password': password,
    }

    response = requests.post(
        f"{baseURL}/register",
        json=payload
    )

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401
    
@app.route('/api_testing')
def api_testing():
    return render_template('testapi.html', **globals())

@app.route('/api/test_mte', methods=['POST'])
def api_test_mte():
    # API URL
    url = f"{baseURL}/myanmar_to_english"
    data= request.get_json()

    # Bearer Token
    token = data.get('token')
    text = data.get('mte')

    # Request headers
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    if not text:
        return jsonify({"error": "Text is required"}), 400
    # Request body
    data = {
        "text": text
    }

    try:
        # Send POST request
        response = requests.post(url, json=data, headers=headers)
        
        # Return response to client
        return jsonify(response.json()), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/test_pte', methods=['POST'])
def api_test_pte():
    # API URL
    url = f"{baseURL}/parli_to_roman"
    data= request.get_json()

    # Bearer Token
    token = data.get('token')
    text = data.get('pte')
    print(f"Received token: {token}, text: {text}")

    # Request headers
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    if not text:
        return jsonify({"error": "Text is required"}), 400
    
    if not token:
        return jsonify({"error": "Token is required"}), 400

    # Request body
    data = {
        "text": text
    }

    try:
        # Send POST request
        response = requests.post(url, json=data, headers=headers)
        
        # Return response to client
        return jsonify(response.json()), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# fun start
if __name__=="__main__":
    app.run(host='0.0.0.0', port=9001, debug=True)
