# Computer Vision · Egg Counting

**YOLOv8m-seg for counting tobacco hornworm (*Manduca sexta*) eggs in laboratory photographs.**

[Русская версия](README.md) · [Methodology](docs/methodology.md) · [Recorded metrics](reports/train/results.csv)

**G. A. Potapov · ITMO University · All-Russian Institute of Plant Protection.**

The workflow combines polygon annotation in CVAT, COCO-to-YOLO conversion, instance segmentation and a Telegram interface. The repository packages the research artifacts with portable inference and training entry points.

| Input | Segmentation output |
|:--:|:--:|
| ![Input](examples/input.jpg) | ![Prediction](docs/assets/prediction.jpg) |

The model detected **28 of 28 annotated eggs** at confidence 0.4. This is a selected successful validation example; aggregate metrics are reported separately below.

## Recorded results

At epoch 74 of the saved `train` run:

| Metric | Boxes | Masks |
|:--|--:|--:|
| Precision | 0.98026 | 0.94350 |
| Recall | 0.96207 | 0.92586 |
| mAP@0.50 | 0.97940 | 0.94344 |
| mAP@0.50:0.95 | 0.83412 | 0.48711 |

These are recorded validation metrics, not counting accuracy or a new independent evaluation. Counting MAE/RMSE have not been measured. The saved run used 100 epochs and patience 200. Epoch 74 has the highest box mAP50 in the saved log; it is not necessarily the epoch selected by the checkpoint fitness criterion.

![Recorded learning curves](docs/assets/results.png)

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python predict.py examples/input.jpg --weights weights/best.pt --device cpu
```

Place the trained **`best.pt`** checkpoint in `weights/`, or supply its path with `--weights`. Model weights are stored separately from the source code. You can also train your own model using the instructions below. Output includes an annotated image and a JSON count. Default inference settings: confidence 0.4, image size 640, maximum 1,000 detections.

For the Telegram interface, set `TELEGRAM_BOT_TOKEN` in the process environment and run `python bot.py`. Never commit tokens. Live Telegram operation has not been tested during packaging.

To train, place YOLO segmentation data under `data/train/{images,labels}` and `data/validation/{images,labels}`, then run:

```bash
python train.py --data configs/data.yaml --epochs 100 --patience 200
```

The dataset contains 172 training and 64 validation images with 15,231 annotated eggs in total. Polygons were annotated in CVAT and converted to the YOLO segmentation format. One example image is included; the full dataset is stored separately.

See [provenance](docs/provenance.md) for third-party tools and packaging changes. No project-wide license has been selected yet.
