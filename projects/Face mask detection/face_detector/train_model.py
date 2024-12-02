import os
import numpy as np
import cv2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam


base_dir = r'C:\Users\Asif\OneDrive\Desktop\Face mask detection\dataset'
  

image_size = (224, 224)

#  ImageDataGenerator to load and preprocess images
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')

validation_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    base_dir,
    target_size=image_size,
    batch_size=32,
    class_mode='binary')

validation_generator = validation_datagen.flow_from_directory(
    base_dir,
    target_size=image_size,
    batch_size=32,
    class_mode='binary')

# Load the MobileNetV2 model pre-trained on ImageNet and exclude the top classification layers
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))


x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
x = Dense(1, activation='sigmoid')(x)  


mask_model = Model(inputs=base_model.input, outputs=x)

for layer in base_model.layers:
    layer.trainable = False

mask_model.compile(optimizer=Adam(learning_rate=1e-4), loss='binary_crossentropy', metrics=['accuracy'])


# model train
mask_model.fit(
    train_generator,
    epochs=10,
    validation_data=validation_generator)

#model save
mask_model.save("mask_detector.h5")  


print("Model training completed and saved as 'mask_detector.model'")
