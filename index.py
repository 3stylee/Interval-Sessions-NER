import time
from flask import Flask, jsonify, request
from flask_cors import CORS
import spacy
from collections import defaultdict
from firebase_admin import credentials, firestore, initialize_app
from getFirebaseKey import getFirebaseKey

# Initialize Firebase
key = getFirebaseKey()
print (key)
cred = credentials.Certificate(key)
initialize_app(cred)
db = firestore.client()

# Load spaCy model
nlp = spacy.load('spacy_model_sm')

app = Flask(__name__)
CORS(app)

NAMED_ENTITIES = ['EFFORT', 'REPETITION']
NON_EFFORTS = ['tempo', 't', 'wu', 'strides', 'primer']

def getToken(req):
    id = req.headers.get('id')
    token = req.headers.get('Authorization')
    if token.startswith('Bearer '):
        token = token[7:]
    else:
        return None, None
    return id, token

def validateToken(req):
    id, token = getToken(req)
    doc_ref = db.collection(u'users').document(id)
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        if data['access_token'] == token and data['expires_at'] > int(time.time()):
            return True
    return False

def create_key(doc):
    entities = [(ent.label_, ent.text.rstrip('m')) for ent in doc.ents if ent.label_ in NAMED_ENTITIES and not any(substring in ent.text.lower() for substring in NON_EFFORTS)]
    efforts = [ent for ent in entities if ent[0] == 'EFFORT']
    reps = [ent for ent in entities if ent[0] == 'REPETITION']
    
    if len(efforts) == len(reps) == 2:
        max_effort_index = entities.index(max(efforts))
        min_effort_index = entities.index(min(efforts))
        if (max_effort_index < min_effort_index):
            rep_index = entities.index(reps[0])
        else:
            rep_index = entities.index(reps[1])
        key = (entities[max_effort_index], entities[rep_index])
    else:
        key = tuple(entities)

    return key

@app.route('/extract_entities', methods=['POST'])
def extract_entities():
    if not validateToken(request):
        return jsonify({'error': 'Invalid authorisation token'}), 401

    data = request.get_json()
    sessions = data['sessions']
    
    groups = defaultdict(list)
    for session in sessions:
        doc = nlp(session['title'])
        key = create_key(doc)
        groups[key].append(session['id'])

    # Convert groups to list of lists for JSON serialization
    results = {str(key): sessions for key, sessions in groups.items()}

    return jsonify(results)

@app.route('/get_key', methods=['POST'])
def get_key():
    if not validateToken(request):
        return jsonify({'error': 'Invalid authorisation token'}), 401

    data = request.get_json()
    session = data['session']
    doc = nlp(session['title'])
    return jsonify(str(create_key(doc)))

if __name__ == '__main__':
    app.run()
