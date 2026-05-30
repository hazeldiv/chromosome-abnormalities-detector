import os
import cv2
from ultralytics import YOLO
import yaml

from dtw_similarity import ChromosomeDTW
from classifier import ChromosomeClassifier

DATASET_PATH = 'dataset'
if os.path.exists(DATASET_PATH):
    print("Dataset Exist")
else:
    print("Dataset Not Exist")

YAML_PATH = 'dataset/data.yaml'

kaggle_yaml = {
    'path': DATASET_PATH,
    'train': 'images/train',
    'val': 'images/val',
    'test': 'images/test',
    'nc': 24,
    'names': {
        0: 'A1', 1: 'A2', 2: 'A3', 3: 'B4', 4: 'B5',
        5: 'C10', 6: 'C11', 7: 'C12', 8: 'C6', 9: 'C7',
        10: 'C8', 11: 'C9', 12: 'D13', 13: 'D14', 14: 'D15',
        15: 'E16', 16: 'E17', 17: 'E18', 18: 'F19', 19: 'F20',
        20: 'G21', 21: 'G22', 22: 'X', 23: 'Y'
    }
}

with open(YAML_PATH, 'w') as f:
    yaml.dump(kaggle_yaml, f, default_flow_style=False, sort_keys=False)


def extract_crop(image, box, padding=5):
    x1, y1, x2, y2 = map(int, box)
    h, w = image.shape[:2]
    x1 = max(0, x1 - padding)
    y1 = max(0, y1 - padding)
    x2 = min(w, x2 + padding)
    y2 = min(h, y2 + padding)
    return image[y1:y2, x1:x2]


def group_detections(results, source_image):
    detections = {}
    for result in results:
        if result.boxes is None:
            continue
        boxes = result.boxes.xyxy.cpu().numpy()
        classes = result.boxes.cls.cpu().numpy()
        for box, cls in zip(boxes, classes):
            cls_id = int(cls)
            if cls_id not in detections:
                detections[cls_id] = []
            crop = extract_crop(source_image, box)
            detections[cls_id].append({'box': box.tolist(), 'image': crop})
    return detections


def main():
    model = YOLO("best.pt")
    dtw_engine = ChromosomeDTW(threshold=0.85)
    classifier = ChromosomeClassifier(dtw_engine)

    data_yaml_path = os.path.abspath(YAML_PATH)
    print(f"Starting YOLO training pipeline using configuration: {data_yaml_path}")

    results = model.train(
        data=data_yaml_path,
        epochs=100,
        imgsz=640,
        lr0=0.0005,
        label_smoothing=0.05,
        batch=-1,
        device=0,
        workers=16,
        save=True,
        project="chromosome_karyotype",
        name="yolo26_24_classes",
        plots=True
    )

    print("\nRunning model against the test set")
    test_results = model.val(
        data=data_yaml_path,
        split="test",
        batch=16,
        imgsz=640,
        save_json=True,
        plots=True
    )

    print("=" * 40)
    print("\n\nTest Set Metric:")
    print("=" * 40)
    print(f"mAP50-95:  {test_results.box.map:.4f}")
    print(f"mAP50:     {test_results.box.map50:.4f}")
    print(f"Precision: {test_results.box.mp:.4f}")
    print(f"Recall:    {test_results.box.mr:.4f}")
    print("=" * 40)
    print(f"Results and curves saved to: {test_results.save_dir}")

    test_images_dir = os.path.join(DATASET_PATH, 'images', 'test')
    if os.path.exists(test_images_dir):
        test_images = [f for f in os.listdir(test_images_dir) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
        total_images = len(test_images)
        all_classifications = []

        print(f"\nClassifying {total_images} test images...")

        for idx, img_name in enumerate(test_images, 1):
            img_path = os.path.join(test_images_dir, img_name)
            image = cv2.imread(img_path)
            if image is None:
                continue

            print(f"  [{idx}/{total_images}] Processing {img_name}...")
            predictions = model.predict(img_path, conf=0.25, verbose=False)
            print(f"         YOLO detected {len(predictions[0].boxes) if predictions[0].boxes is not None else 0} objects")
            detections = group_detections(predictions, image)
            classification = classifier.classify(detections)
            classification['image'] = img_name
            all_classifications.append(classification)
            print(f"         Classification complete: {len(classification['normal'])} normal, {len(classification['ambiguous'])} ambiguous")

        output_path = os.path.join("output", "classification_results.json")
        os.makedirs("output", exist_ok=True)
        classifier.save_results({'images': all_classifications}, output_path)
        print(f"\nClassification results saved to: {output_path}")

        for cls in all_classifications:
            classifier.print_summary(cls)


if __name__ == "__main__":
    main()