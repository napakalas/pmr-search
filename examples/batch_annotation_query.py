import argparse
import json
from pathlib import Path

from tqdm import tqdm

from pmr_search import ModelSearch


def parse_args():
    parser = argparse.ArgumentParser(description="Batch PMR search from an annotation JSON file")
    parser.add_argument("--source", default="examples/annotation.example.json", help="Input annotation JSON")
    parser.add_argument("--dest", default="examples/annotation.out.json", help="Output JSON with pmr field")
    parser.add_argument("--topk", type=int, default=5)
    parser.add_argument("--min-sim", type=float, default=0.84)
    return parser.parse_args()


def main():
    args = parse_args()
    source = Path(args.source)
    dest = Path(args.dest)

    with source.open("r", encoding="utf-8") as fp:
        annotations = json.load(fp)

    ms = ModelSearch()
    try:
        for values in annotations.values():
            for ann in tqdm(values):
                term_id = ann.get("Model", "") + ann.get("Models", "")
                context = ann.get("Organ", "") + ann.get("Organ/System", "")
                candidates = ms.search(
                    term_id,
                    context=[context, "Human"],
                    topk=args.topk,
                    min_sim=args.min_sim,
                    c_weight=1,
                )
                if candidates:
                    model = candidates[0]
                    pmr_model = (model["exposure"] + model["workspace"] + model["cellml"])[0]
                    ann["pmr"] = {"score": model["score"], "pmr_model": pmr_model}
    finally:
        ms.close()

    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("w", encoding="utf-8") as fp:
        json.dump(annotations, fp, indent=2)

    print(f"Saved: {dest}")


if __name__ == "__main__":
    main()
