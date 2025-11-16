import os, time, glob, pandas as pd, mlflow, argparse, shutil
from pathlib import Path
from ultralytics import YOLO

def latest_run_dir(base="runs/detect"):
    paths = sorted(Path(base).glob("*"), key=lambda p: p.stat().st_mtime)
    return paths[-1] if paths else None

def log_yolo_artifacts(run_dir):
    for f in ["results.png", "confusion_matrix.png", "PR_curve.png", "labels_correlogram.jpg"]:
        p = Path(run_dir) / f
        if p.exists():
            mlflow.log_artifact(str(p), artifact_path="yolo_plots")
    best = Path(run_dir) / "weights" / "best.pt"
    if best.exists():
        mlflow.log_artifact(str(best), artifact_path="weights")

def log_yolo_metrics(run_dir):
    csv_path = Path(run_dir) / "results.csv"
    if not csv_path.exists():
        return
    df = pd.read_csv(csv_path)
    last = df.iloc[-1].to_dict()
    for k in ["metrics/precision(B)", "metrics/recall(B)", "metrics/mAP50(B)", "metrics/mAP50-95(B)"]:
        if k in last:
            mlflow.log_metric(k.replace("(B)", ""), float(last[k]))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/tiny_coco.yaml")
    ap.add_argument("--model", default="yolov8n.pt")  # ou "yolo11n.pt" selon install
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--imgsz", type=int, default=320)
    ap.add_argument("--lr0", type=float, default=0.005)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--exp-name", default="cv_yolo_tiny")
    args = ap.parse_args()

    mlflow.set_experiment(args.exp_name)
    run_name = f"{Path(args.model).stem}_e{args.epochs}_sz{args.imgsz}_lr{args.lr0}_s{args.seed}"
    with mlflow.start_run(run_name=run_name):
        # log params / tags
        mlflow.log_params({
            "model": args.model, "epochs": args.epochs, "imgsz": args.imgsz,
            "lr0": args.lr0, "batch": args.batch, "seed": args.seed, "data": args.data
        })
        mlflow.set_tags({"task": "object-detection", "dataset": "tiny_coco_person"})

        # train
        model = YOLO(args.model)
        model.train(
            data=args.data,
            epochs=args.epochs,
            imgsz=args.imgsz,
            lr0=args.lr0,
            batch=args.batch,
            seed=args.seed,
            project="runs",
            name=run_name,
            verbose=False
        )

        run_dir = Path("runs/detect") / run_name
        if not run_dir.exists():
            run_dir = latest_run_dir()  

        # log metrics + artifacts
        if run_dir:
            log_yolo_metrics(run_dir)
            log_yolo_artifacts(run_dir)

if __name__ == "__main__":
    main()
