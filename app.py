from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import json

app = Flask(__name__)

# ---------------- LOAD MODEL ----------------
model = tf.keras.models.load_model("fruit_classifier_model.keras")

IMG_SIZE = 100

# ---------------- LOAD CLASS LABELS ----------------
with open("class_labels.json", "r") as f:
    class_indices = json.load(f)

# Reverse mapping: index → class name
index_to_class = {v: k for k, v in class_indices.items()}

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]

    # Preprocess image
    img = Image.open(file).convert("RGB")
    img = img.resize((IMG_SIZE, IMG_SIZE))
    img_array = np.array(img, dtype=np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict
    prediction = model.predict(img_array, verbose=0)
    confidence = float(np.max(prediction) * 100)
    class_index = int(np.argmax(prediction))
    fruit = index_to_class[class_index]
    print("Top 5 probabilities:")
    top5 = np.argsort(prediction[0])[-5:][::-1]
    for i in top5:
        print(index_to_class[i], prediction[0][i])


    return jsonify({
        "fruit": fruit,
        "confidence": round(confidence, 2)
    })

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)
