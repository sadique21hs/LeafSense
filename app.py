from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import traceback

app = Flask(__name__)

# --- Configuration ---
UPLOAD_FOLDER = 'uploads'
MODEL_PATH = 'plant_disease_model.h5'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Load Model Safely ---
try:
    model = load_model(MODEL_PATH)
    print(f"✅ Successfully loaded model from {MODEL_PATH}")
except Exception as e:
    print(f"⚠️ Error loading model: {e}")
    print("➡️ Using dummy predictor for testing.")

    def dummy_predict(img_array):
        print("🧪 Using DUMMY PREDICTION (Model not loaded).")
        # Always predicts class 10 (Corn___Northern_Leaf_Blight)
        dummy_output = np.zeros((1, 23))
        dummy_output[0, 10] = 1.0
        return dummy_output

    model = type("DummyModel", (), {"predict": dummy_predict})()


# --- Define Class Names (23 classes) ---
class_names = [
    'Apple___Apple_scab',
    'Apple___Black_rot',
    'Apple___Cedar_apple_rust',
    'Apple___Healthy',
    'Blueberry___Healthy',
    'Cherry___Healthy',
    'Cherry___Powdery_mildew',
    'Corn___Cercospora_leaf_spot',
    'Corn___Common_rust',
    'Corn___Healthy',
    'Corn___Northern_Leaf_Blight',
    'Grape___Black_rot',
    'Grape___Esca',
    'Grape___Healthy',
    'Grape___Leaf_blight',
    'Orange___Haunglongbing',
    'Peach___Bacterial_spot',
    'Peach___Healthy',
    'Pepper_bell___Bacterial_spot',
    'Pepper_bell___Healthy',
    'Potato___Early_blight',
    'Potato___Healthy',
    'Potato___Late_blight'
]

# --- Treatments Dictionary ---
treatments = {
    "Apple___Apple_scab": "Take off bad leaves. Spray medicine. Give space to plants.",
    "Apple___Black_rot": "Cut bad branches. Use copper spray. Don’t water from the top.",
    "Apple___Cedar_apple_rust": "Remove cedar trees. Spray sulfur or copper early.",
    "Apple___Healthy": "No care needed. Keep soil and water good.",

    "Corn___Healthy": "No care needed. Keep watching plants.",
    "Corn___Common_rust": "Plant strong corn. Spray when rust starts.",
    "Corn___Northern_Leaf_Blight": "Plant strong corn. Spray if it gets worse.",
    "Corn___Cercospora_leaf_spot": "Change crops. Spray if needed.",

    "Potato___Healthy": "No care needed.",
    "Potato___Late_blight": "Remove bad plants. Spray medicine.",
    "Potato___Early_blight": "Change crops. Spray medicine.",

    "Pepper_bell___Bacterial_spot": "Remove bad leaves. Spray copper. Don’t touch wet plants.",
    "Pepper_bell___Healthy": "Plant is healthy!",

    "Grape___Black_rot": "Cut bad parts. Spray medicine.",
    "Grape___Esca": "Cut bad wood. Don’t cut too much.",
    "Grape___Healthy": "No care needed.",
    "Grape___Leaf_blight": "Spray medicine. Take off bad leaves.",

    "Orange___Haunglongbing": "No cure. Remove bad trees. Stop insects.",
    "Peach___Bacterial_spot": "Spray copper. Plant strong trees.",
    "Peach___Healthy": "No care needed.",

    "Cherry___Powdery_mildew": "Spray sulfur. Cut for more air.",
    "Cherry___Healthy": "No care needed.",

    "Blueberry___Healthy": "Plant is healthy. Keep soil dry and water well."
}


# --- File Validation ---
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# --- Routes ---
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded.'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected.'})

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload JPG, JPEG, PNG, or GIF.'})

    filepath = None
    try:
        # Save uploaded file
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Preprocess image
        img = image.load_img(filepath, target_size=(128, 128))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        # Predict
        predictions = model.predict(img_array)
        probabilities = predictions[0]
        predicted_index = int(np.argmax(probabilities))
        predicted_class = class_names[predicted_index]
        confidence = float(probabilities[predicted_index] * 100)

         # --- Random / unrelated image handling ---
        if confidence < 60:
            status = "uncertain"
            message = "⚠️ This image is unclear. Please upload a leaf image."
            predicted_class = "Unknown"
            treatment = "Cannot detect any leaf disease. Please try again with a clear leaf photo."
        elif confidence < 85:
            status = "warning"
            message = "⚠️ Model is unsure. This might not be a leaf image."
            predicted_class = "Possibly not a plant image"
            treatment = "Please upload a clear photo of a single plant leaf."
        else:
            status = "success"
            message = "✅ Prediction successful!"
            treatment = treatments.get(predicted_class, "Treatment information not available.")

        print(f"🪴 Predicted: {predicted_class} | Confidence: {confidence:.2f}%")

        return jsonify({
            'prediction': predicted_class,
            'confidence': round(confidence, 2),
            'message': message,
            'status': status,
            'treatment': treatments.get(predicted_class, "Treatment information not available.")
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'⚠️ Server error during prediction: {str(e)}'})

    finally:
        if filepath and os.path.exists(filepath):
            try:
                os.remove(filepath)
            except OSError as e:
                print(f"Error removing file {filepath}: {e}")


# --- Run Server ---
if __name__ == '__main__':
    app.run(debug=True)
