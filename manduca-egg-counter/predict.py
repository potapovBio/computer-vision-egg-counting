"""Count Manduca sexta eggs in one local image using trained YOLO weights."""
import argparse
import json
from pathlib import Path


def predict(weights, source, output, conf=0.4, device=None):
    import cv2
    from ultralytics import YOLO

    weights, source, output = Path(weights), Path(source), Path(output)
    if not weights.is_file():
        raise FileNotFoundError(f"Trained weights not found: {weights}")
    if not source.is_file():
        raise FileNotFoundError(f"Image not found: {source}")
    image = cv2.imread(str(source))
    if image is None:
        raise ValueError(f"Cannot decode image: {source}")
    model = YOLO(str(weights))
    if model.task != "segment" or set(model.names.values()) != {"egg"}:
        raise ValueError("Expected a single-class egg segmentation model")
    result = model.predict(image, imgsz=640, conf=conf, classes=[0],
                           device=device, verbose=False, max_det=1000)[0]
    count = 0 if result.boxes is None else len(result.boxes)
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.resolve() == source.resolve():
        raise ValueError("Output must differ from the input image")
    if not cv2.imwrite(str(output), result.plot(labels=False, line_width=1)):
        raise OSError(f"Cannot write output: {output}")
    return {"count": count, "confidence": conf, "image_size": 640,
            "max_detections": 1000, "source": source.name, "output": str(output)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--weights", type=Path, default=Path("weights/best.pt"))
    parser.add_argument("--output", type=Path, default=Path("outputs/prediction.jpg"))
    parser.add_argument("--conf", type=float, default=0.4)
    parser.add_argument("--device", default=None, help="cpu, mps, or CUDA device index")
    args = parser.parse_args()
    if not 0 <= args.conf <= 1:
        parser.error("--conf must be between 0 and 1")
    try:
        summary = predict(args.weights, args.source, args.output, args.conf, args.device)
    except (FileNotFoundError, ValueError, OSError) as exc:
        parser.exit(1, f"{exc}\n")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
