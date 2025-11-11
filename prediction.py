import cv2
import numpy as np

def preprocess_image(image_path, image_size=(150,150)):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, image_size)
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def predict_and_get_class_images(image_path, model, class_names_dict):
    img = preprocess_image(image_path)
    predictions = model.predict(img)
    pred_idx = np.argmax(predictions[0])
    pred_class = class_names_dict[str(pred_idx)]
    confidence = predictions[0][pred_idx]
    return pred_class, float(confidence)