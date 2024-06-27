from processData import processData
import tensorflow as tf
import numpy as np

ACTIVITY_LABEL_MAPPING = {
	0: "Easy",
	1: "Long Run",
	2: "Race",
	3: "Session",
	4: "Tempo",
}

def predictData(data):
    results = []
    processed_data = processData(data)
    model = tf.keras.models.load_model("model.h5")  # Adjust the path to your model

    for i, row in enumerate(processed_data):
        if data[i]['type'] != 'Run':
            results.append(data[i]['type'])
        else:
            tensor_data = tf.constant([row], dtype=tf.float32)
            prediction = model.predict(tensor_data)
            predicted_class_index = np.argmax(prediction, axis=1)[0]
            results.append(ACTIVITY_LABEL_MAPPING[predicted_class_index])
    return results
