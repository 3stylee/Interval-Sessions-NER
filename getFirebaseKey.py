from dotenv import load_dotenv
import os
import json

def getFirebaseKey():
    with open('firebaseKey.json', 'r') as file:
        firebase_config_template = file.read()

    load_dotenv()
    # Replace placeholders with environment variables
    firebase_config_json = firebase_config_template\
        .replace('$PRIVATE_KEY_ID', os.getenv('FIREBASE_PRIVATE_KEY_ID'))\
        .replace('$PRIVATE_KEY', os.getenv('FIREBASE_PRIVATE_KEY'))\
        .replace('$CLIENT_EMAIL', os.getenv('FIREBASE_CLIENT_EMAIL'))\
        .replace('$CLIENT_ID', os.getenv('FIREBASE_CLIENT_ID'))

    return json.loads(firebase_config_json)