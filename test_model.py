from tensorflow.keras.models import load_model
import numpy as np

# Load your trained model
model = load_model('plant_disease_model.h5')

# Create a dummy image with correct shape (adjust size if needed)
dummy = np.random.rand(1, 224, 224, 3)
pred = model.predict(dummy)

print("✅ Model loaded successfully!")
print("Prediction output:", pred)
print("Output shape:", pred.shape)
