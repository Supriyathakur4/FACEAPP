import cv2
import os
import numpy as np

# Path to dataset
dataset_path = "dataset"

# Create LBPH recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

faces = []
labels = []

FACE_SIZE = (200, 200)  # fixed size required for LBPH

# Read dataset
for user_id in os.listdir(dataset_path):
    user_path = os.path.join(dataset_path, user_id)

    if not os.path.isdir(user_path):
        continue

    for image_name in os.listdir(user_path):
        image_path = os.path.join(user_path, image_name)

        # Read image in grayscale
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # Skip invalid images
        if img is None:
            print("Skipping:", image_path)
            continue

        # Resize image
        img = cv2.resize(img, FACE_SIZE)

        faces.append(img)
        labels.append(int(user_id))

# Convert labels to NumPy int32 array (IMPORTANT)
labels = np.array(labels, dtype=np.int32)

print("Total faces:", len(faces))
print("Total labels:", len(labels))
print("Labels dtype:", labels.dtype)

# Safety check
if len(faces) == 0:
    raise ValueError("No face images found. Training aborted.")

# Train the model
recognizer.train(faces, labels)

# Save trained model
recognizer.save("trainer.yml")

print("✅ Training completed and model saved as trainer.yml")



