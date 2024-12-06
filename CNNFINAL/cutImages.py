import cv2
import os
import re

def extract_car_frames(video_path, output_dir, frame_interval=50, image_size=(80, 80)):
    # Cargar el modelo YOLO preentrenado
    net = cv2.dnn.readNet("C:/Users/angel/OneDrive/Escritorio/IA/CNNFINAL/yolov3.weights", "C:/Users/angel/OneDrive/Escritorio/IA/CNNFINAL/yolov3.cfg")  # Reemplaza con tu modelo YOLO
    layer_names = net.getLayerNames()
    if isinstance(net.getUnconnectedOutLayers(), (list, tuple)):
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    else:
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    # Cargar las clases del modelo
    with open("C:/Users/angel/OneDrive/Escritorio/IA/CNNFINAL/coco.names", "r") as f:  # Asegúrate de que coco.names contiene "car"
        classes = f.read().strip().split("\n")

    # Crear la carpeta de salida si no existe
    os.makedirs(output_dir, exist_ok=True)

    existing_files = [f for f in os.listdir(output_dir) if f.startswith("mini_") and f.endswith(".jpg")]
    if existing_files:
        last_index = max([int(re.search(r"(\d+)", f).group()) for f in existing_files])
    else:
        last_index = -1  

    frame_count = last_index + 1  # 

    cap = cv2.VideoCapture(video_path)
    count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if count % frame_interval == 0:
            height, width, _ = frame.shape
            
            # Crear blob para YOLO
            blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
            net.setInput(blob)
            detections = net.forward(output_layers)

            car_detected = False  
            for detection in detections:
                for obj in detection:
                    scores = obj[5:]
                    class_id = int(scores.argmax())
                    confidence = scores[class_id]
                    
                    if classes[class_id] == "car" and confidence > 0.5:  # Filtrar solo coches
                        car_detected = True  # Se detectó al menos un coche

                        center_x, center_y, w, h = (obj[0:4] * [width, height, width, height]).astype("int")
                        x = max(0, int(center_x - w / 2))
                        y = max(0, int(center_y - h / 2))
                        w = min(w, width - x)
                        h = min(h, height - y)
                        
                        if w > 0 and h > 0:
                            cropped_car = frame[y:y+h, x:x+w]
                            
                            # Redimensionar a 80x80
                            resized_car = cv2.resize(cropped_car, image_size)
                            
                            frame_name = os.path.join(output_dir, f"vocho_{frame_count:05d}.jpg")  
                            cv2.imwrite(frame_name, resized_car)
                            frame_count += 1
                            print(f"Saved {frame_name}")
            
            if not car_detected:
                print(f"No cars detected in frame {count}")

        count += 1

    cap.release()
    print(f"Extracted {frame_count - (last_index + 1)} car frames to {output_dir}")

# Ejemplo de uso
extract_car_frames(
    video_path="C:/Users/angel/OneDrive/Escritorio/IA/CNNFINALcnn/newvideos/ferrari f40/37.mp4",
    output_dir="C:/Users/angel/OneDrive/Escritorio/IA/CNNFINALcnn/dataset/ferrari f4037",
    frame_interval=50,  # Extrae un frame cada 50 frames
    image_size=(80, 80)  # Redimensiona a 80x80
)   