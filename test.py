import spacy

# Load your trained model
nlp = spacy.load('spacy_model_sm')

# List of sentences to test
sentences = [
    "2 x 200m on, off WU, 18 x 200m every 90s",
    "2 x 200m on, off, 3 x 1600m every 8 mins"
]
NAMED_ENTITIES = ['EFFORT', 'REPETITION']
NON_EFFORTS = ['tempo', 't', 'wu', 'strides', 'primer']

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

# Process the sentences
for sentence in sentences:
    doc = nlp(sentence)
    key = create_key(doc)

    print(f"Key for '{sentence}': {key}")
    print('\n')