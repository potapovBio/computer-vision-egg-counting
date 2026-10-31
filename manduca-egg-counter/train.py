"""Train with explicit dataset paths and recorded experiment parameters."""
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("configs/data.yaml"))
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--patience", type=int, default=200)
    parser.add_argument("--device", default=None)
    args = parser.parse_args()
    if not args.data.is_file():
        parser.error(f"Dataset configuration not found: {args.data}")
    from ultralytics import YOLO
    YOLO("yolov8m-seg.pt").train(
        data=str(args.data.resolve()), epochs=args.epochs, patience=args.patience,
        imgsz=640, batch=8, device=args.device, seed=0,
        project="runs/segment", name="manduca", exist_ok=False,
    )


if __name__ == "__main__":
    main()
