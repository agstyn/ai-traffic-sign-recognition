import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout, BatchNormalization
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import warnings
warnings.filterwarnings('ignore')

# ── Config ────────────────────────────────────────────────
TRAIN_PATH  = "data/GTSRB/Final_Training/Images"
MODEL_PATH  = "models/traffic_sign_model.h5"
IMG_SIZE    = 32
NUM_CLASSES = 43
BATCH_SIZE  = 64
EPOCHS      = 20
RANDOM_SEED = 42

# ── Class Names ───────────────────────────────────────────
CLASS_NAMES = [
    "Speed limit 20", "Speed limit 30", "Speed limit 50",
    "Speed limit 60", "Speed limit 70", "Speed limit 80",
    "End speed limit 80", "Speed limit 100", "Speed limit 120",
    "No passing", "No passing >3.5t", "Right of way",
    "Priority road", "Yield", "Stop", "No vehicles",
    "No vehicles >3.5t", "No entry", "General caution",
    "Dangerous curve left", "Dangerous curve right", "Double curve",
    "Bumpy road", "Slippery road", "Road narrows right",
    "Road work", "Traffic signals", "Pedestrians", "Children crossing",
    "Bicycles crossing", "Ice/snow", "Wild animals crossing",
    "End restrictions", "Turn right ahead", "Turn left ahead",
    "Ahead only", "Go straight or right", "Go straight or left",
    "Keep right", "Keep left", "Roundabout", "End no passing",
    "End no passing >3.5t"
]

print("=" * 50)
print("  TRAFFIC SIGN RECOGNITION — CNN TRAINER")
print("=" * 50)

# ── Step 1: Load Images ───────────────────────────────────
print("\n[1/5] Loading images...")
images, labels = [], []
class_folders = sorted(os.listdir(TRAIN_PATH))

for idx, folder in enumerate(class_folders):
    folder_path = os.path.join(TRAIN_PATH, folder)
    for img_file in os.listdir(folder_path):
        if img_file.endswith('.ppm'):
            try:
                img = Image.open(os.path.join(folder_path, img_file))
                img = img.resize((IMG_SIZE, IMG_SIZE))
                images.append(np.array(img))
                labels.append(idx)
            except:
                pass

images = np.array(images)
labels = np.array(labels)
print(f"    Loaded {len(images)} images across {NUM_CLASSES} classes")

# ── Step 2: Preprocess ────────────────────────────────────
print("\n[2/5] Preprocessing...")
images = images / 255.0
labels_cat = to_categorical(labels, NUM_CLASSES)

X_train, X_val, y_train, y_val = train_test_split(
    images, labels_cat,
    test_size=0.2,
    random_state=RANDOM_SEED,
    stratify=labels
)
print(f"    Train: {len(X_train)} | Validation: {len(X_val)}")

# ── Step 3: Build CNN ─────────────────────────────────────
print("\n[3/5] Building CNN model...")

model = Sequential([
    # Block 1
    Conv2D(32, (3,3), activation='relu', padding='same', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
    BatchNormalization(),
    Conv2D(32, (3,3), activation='relu', padding='same'),
    MaxPooling2D(2, 2),
    Dropout(0.25),

    # Block 2
    Conv2D(64, (3,3), activation='relu', padding='same'),
    BatchNormalization(),
    Conv2D(64, (3,3), activation='relu', padding='same'),
    MaxPooling2D(2, 2),
    Dropout(0.25),

    # Block 3
    Conv2D(128, (3,3), activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling2D(2, 2),
    Dropout(0.25),

    # Classifier
    Flatten(),
    Dense(512, activation='relu'),
    BatchNormalization(),
    Dropout(0.5),
    Dense(NUM_CLASSES, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ── Step 4: Train ─────────────────────────────────────────
print("\n[4/5] Training...")

callbacks = [
    EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True),
    ModelCheckpoint(MODEL_PATH, monitor='val_accuracy', save_best_only=True, verbose=1)
]

history = model.fit(
    X_train, y_train,
    batch_size=BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=(X_val, y_val),
    callbacks=callbacks,
    verbose=1
)

# ── Step 5: Save Visualizations ───────────────────────────
print("\n[5/5] Saving training charts...")
os.makedirs("data", exist_ok=True)

# Accuracy chart
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Train Accuracy', color='steelblue')
plt.plot(history.history['val_accuracy'], label='Val Accuracy', color='orange')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

# Loss chart
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Train Loss', color='steelblue')
plt.plot(history.history['val_loss'], label='Val Loss', color='orange')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.tight_layout()
plt.savefig("data/training_history.png")
plt.show()
print("    Training chart saved to data/training_history.png")

# Confusion matrix on validation set
print("\n    Generating confusion matrix...")
y_pred = model.predict(X_val, verbose=0)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true_classes = np.argmax(y_val, axis=1)

cm = confusion_matrix(y_true_classes, y_pred_classes)
plt.figure(figsize=(20, 18))
sns.heatmap(cm, annot=False, fmt='d', cmap='Blues',
            xticklabels=range(NUM_CLASSES),
            yticklabels=range(NUM_CLASSES))
plt.title('Confusion Matrix')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.tight_layout()
plt.savefig("data/confusion_matrix.png")
plt.show()
print("    Confusion matrix saved to data/confusion_matrix.png")

# Classification report
report = classification_report(y_true_classes, y_pred_classes, target_names=CLASS_NAMES)
with open("data/classification_report.txt", "w") as f:
    f.write(report)
print("    Classification report saved to data/classification_report.txt")

print("\n" + "=" * 50)
print("  TRAINING COMPLETE!")
print(f"  Model saved to: {MODEL_PATH}")
print("=" * 50)