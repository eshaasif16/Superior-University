import os
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from imutils.video import VideoStream
import imutils
import time

def detect_and_predict_mask(frame, faceNet, maskNet):
   
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224), (104.0, 177.0, 123.0))

    faceNet.setInput(blob)
    detections = faceNet.forward()

    # initialize lists for faces, their locations, and predictions
    faces = []
    locs = []
    preds = []

    # Loop over the detections
    for i in range(0, detections.shape[2]):
       
        confidence = detections[0, 0, i, 2]

        # Filter out weak detections
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

          
            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

         
            face = frame[startY:endY, startX:endX]
            if face.size > 0:
                face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                face = cv2.resize(face, (224, 224))
                face = img_to_array(face)
                face = preprocess_input(face)

                faces.append(face)
                locs.append((startX, startY, endX, endY))

    # If faces are detected, predict masks, else return empty lists
    if len(faces) > 0:
        faces = np.array(faces, dtype="float32")
        preds = maskNet.predict(faces, batch_size=32)
        print("Predictions shape:", preds.shape)  
        print("Predictions content:", preds)  
        
        # ensure preds is 2D for mask and without mask 
        if preds.shape[1] == 1:
            preds = np.hstack([preds, 1 - preds])  
        
        return locs, preds
    else:
        return locs, []  #if no face detect then empty pred will be returned

prototxtPath = r"C:\Users\Asif\OneDrive\Desktop\Face mask detection\face_detector\deploy.prototxt"
weightsPath = r"C:\Users\Asif\OneDrive\Desktop\Face mask detection\face_detector\res10_300x300_ssd_iter_140000.caffemodel"

if not os.path.exists(prototxtPath):
    print(f"Error: {prototxtPath} does not exist!")
if not os.path.exists(weightsPath):
    print(f"Error: {weightsPath} does not exist!")

faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

# load the face mask detector model
mask_model_path = r"C:\Users\Asif\OneDrive\Desktop\Face mask detection\mask_detector.h5" 
if not os.path.exists(mask_model_path):
    raise FileNotFoundError("Mask detector model file not found!")

maskNet = load_model(mask_model_path)

# initialize the video stream
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)  #camera warm up

try:
    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        # will detect faces and predict mask usage
        (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)

        # if no faces detected then preds will be empty
        if len(locs) > 0 and len(preds) > 0:
            # Loop over the detected faces and predictions
            for (box, pred) in zip(locs, preds):
                (startX, startY, endX, endY) = box
                mask, withoutMask = pred  # pred is an array with two values: [mask, no_mask]

                # debugging
                print(f"Mask: {mask}, No Mask: {withoutMask}")

                # label and color mask no mask
                label = "Mask" if mask > withoutMask else "No Mask"
                color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
                label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

                # label display
                cv2.putText(frame, label, (startX, startY - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
                cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

       
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

       
        if key == ord("q"):
            break
except KeyboardInterrupt:
    print("[INFO] Exiting due to keyboard interrupt")
except Exception as e:
    print(f"[ERROR] An error occurred: {e}")
finally:
    print("[INFO] Cleaning up...")
    cv2.destroyAllWindows()
    vs.stop()
