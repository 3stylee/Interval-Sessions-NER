from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy
from collections import defaultdict
from predictData import predictData

# Load your trained spaCy model
nlp = spacy.load('spacy_model_sm')

app = Flask(__name__)
CORS(app)

NAMED_ENTITIES = ['EFFORT', 'REPETITION']
NON_EFFORTS = ['tempo', 't', 'wu', 'strides', 'primer']

def create_key(doc, groups, session):
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

    groups[key].append(session['id'])

@app.route('/extract_entities', methods=['POST'])
def extract_entities():
    data = request.get_json()
    sessions = data['sessions']
    
    groups = defaultdict(list)

    for session in sessions:
        doc = nlp(session['title'])
        create_key(doc, groups, session)

    # Convert groups to list of lists for JSON serialization
    results = [sessions for sessions in groups.values()]

    return jsonify(results)

@app.route('/predict_type', methods=['POST'])
def predict_type():
    data = request.get_json()
    activities = data['activities']

    results = predictData(activities)

    return jsonify(results)

if __name__ == '__main__':
    app.run()
