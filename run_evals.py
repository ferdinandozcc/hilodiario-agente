"""Evals como puerta de calidad: si la puntuación media baja del umbral, el pipeline falla.

Uso: python evals/run_evals.py --threshold 0.8
"""
import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.agent import summarize  # noqa: E402


def score_case(case: dict) -> float:
    output = summarize(case["input"], max_words=case["max_words"])
    checks = [len(output.split()) <= case["max_words"]]
    checks += [kw.lower() in output.lower() for kw in case["must_include"]]
    return sum(checks) / len(checks)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", type=float, default=0.8)
    args = parser.parse_args()

    cases = json.loads((Path(__file__).parent / "cases.json").read_text(encoding="utf-8"))
    scores = {c["id"]: score_case(c) for c in cases}
    for case_id, s in scores.items():
        print(f"{case_id}: {s:.2f}")
    mean = sum(scores.values()) / len(scores)
    print(f"Media: {mean:.2f} (umbral {args.threshold})")

    # Resumen visible en la pestaña Actions de GitHub (métricas en cada cambio)
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        estado = "OK" if mean >= args.threshold else "FALLO"
        lines = ["## Evals del agente", "", "| Caso | Puntuación |", "|---|---|"]
        lines += [f"| {cid} | {sc:.2f} |" for cid, sc in scores.items()]
        lines += ["", f"**Media: {mean:.2f}** (umbral {args.threshold}) · **{estado}**"]
        with open(summary_path, "a", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
    if mean < args.threshold:
        print("FALLO: la calidad del agente está por debajo del umbral")
        return 1
    print("OK: la calidad del agente cumple el umbral")
    return 0


if __name__ == "__main__":
    sys.exit(main())
