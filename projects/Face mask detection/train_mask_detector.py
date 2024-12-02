
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import AveragePooling2D, Dropout, Flatten, Dense, Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import numpy as np
import os

# Initialize the learning rate, number of epochs, and batch size
INIT_LR = 1e-4
EPOCHS = 20
BS = 32

DIRECTORY = r"C:\\Users\\Asif\\OneDrive\\Desktop\\Face mask detection\\dataset"
CATEGORIES = ["with_mask", "without_mask"]

# Initialize data and labels lists
data = []
labels = []

print("[INFO] Loading images...")

# Loop through categories and load images
for category in CATEGORIES:
    path = os.path.join(DIRECTORY, category)
    if not os.path.exists(path):
        print(f"[ERROR] Path does not exist: {path}")
        continue

    for img in os.listdir(path):
        img_path = os.path.join(path, img)
        try:
            # Load, preprocess, and append the image data
            image = load_img(img_path, target_size=(224, 224))
            image = img_to_array(image)
            image = preprocess_input(image)

            data.append(image)
            labels.append(category)
        except Exception as e:
            print(f"[ERROR] Could not process image {img_path}: {e}")

# Check if data and labels are populated
if len(data) == 0 or len(labels) == 0:
    raise ValueError("[ERROR] No data or labels found. Check your dataset directory structure.")

# Perform one-hot encoding on the labels
print("[INFO] Encoding labels...")
lb = LabelBinarizer()
labels = lb.fit_transform(labels)
labels = to_categorical(labels)

data = np.array(data, dtype="float32")
labels = np.array(labels)

# Split data into training and testing sets
(trainX, testX, trainY, testY) = train_test_split(
    data, labels, test_size=0.20, stratify=labels, random_state=42
)

# Construct the training image generator for data augmentation
aug = ImageDataGenerator(
    rotation_range=20,
    zoom_range=0.15,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.15,
    horizontal_flip=True,
    fill_mode="nearest",
)

# Load the MobileNetV2 network, ensuring the head FC layers are left off
baseModel = MobileNetV2(weights="imagenet", include_top=False, input_tensor=Input(shape=(224, 224, 3)))

# Construct the head of the model
headModel = baseModel.output
headModel = AveragePooling2D(pool_size=(7, 7))(headModel)
headModel = Flatten(name="flatten")(headModel)
headModel = Dense(128, activation="relu")(headModel)
headModel = Dropout(0.5)(headModel)
headModel = Dense(2, activation="softmax")(headModel)

# Place the head FC model on top of the base model
model = Model(inputs=baseModel.input, outputs=headModel)

# Freeze the base model layers
for layer in baseModel.layers:
    layer.trainable = False

# Compile the model
print("[INFO] Compiling model...")
opt = Adam(learning_rate=INIT_LR, decay=INIT_LR / EPOCHS)
model.compile(loss="binary_crossentropy", optimizer=opt, metrics=["accuracy"])

# Train the head of the network
print("[INFO] Training head...")
validation_steps = max(1, len(testX) // BS)  # Ensure validation steps are valid
H = model.fit(
    aug.flow(trainX, trainY, batch_size=BS),
    steps_per_epoch=len(trainX) // BS,
    validation_data=(testX, testY),
    validation_steps=validation_steps,
    epochs=EPOCHS,
)

# Evaluate the network
print("[INFO] Evaluating network...")
predIdxs = model.predict(testX, batch_size=BS)
predIdxs = np.argmax(predIdxs, axis=1)

# Show a nicely formatted classification report
print(classification_report(testY.argmax(axis=1), predIdxs, target_names=lb.classes_))

# Save the model to disk
print("[INFO] Saving mask detector model...")
model.save("mask_detector.h5")

# Plot the training loss and accuracy
N = len(H.history["loss"])  # Get the actual number of recorded epochs
plt.style.use("ggplot")
plt.figure()

# Dynamically match the lengths of each metric
plt.plot(np.arange(len(H.history["loss"])), H.history["loss"], label="train_loss")
plt.plot(np.arange(len(H.history["val_loss"])), H.history["val_loss"], label="val_loss")
plt.plot(np.arange(len(H.history["accuracy"])), H.history["accuracy"], label="train_acc")
plt.plot(np.arange(len(H.history["val_accuracy"])), H.history["val_accuracy"], label="val_acc")

# Add titles and labels
plt.title("Training Loss and Accuracy")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="lower left")

# Save and display the plot
plt.savefig("plot.png")
plt.show()

