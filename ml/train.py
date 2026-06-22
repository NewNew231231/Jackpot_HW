import os
import random
import pandas as pd
import mlflow

from app.config import MLFLOW_TRACKING_URI, TRIAL_COUNT, SYMBOLS


BASE_DIR = os.path.dirname(__file__)
ARTIFACT_DIR = os.path.join(BASE_DIR, "artifacts")
RESULT_PATH = os.path.join(ARTIFACT_DIR, "jackpot_result.csv")

os.makedirs(ARTIFACT_DIR, exist_ok=True)


def spin_jackpot():
    result = [
        random.choice(SYMBOLS),
        random.choice(SYMBOLS),
        random.choice(SYMBOLS)
    ]

    jackpot = result[0] == result[1] == result[2]

    return result, jackpot


mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("jackpot-simulation-ngrok")


with mlflow.start_run(run_name="jackpot_simulation"):
    mlflow.log_param("project", "jackpot")
    mlflow.log_param("symbol_count", len(SYMBOLS))
    mlflow.log_param("trial_count", TRIAL_COUNT)

    records = []
    jackpot_count = 0

    for i in range(TRIAL_COUNT):
        result, jackpot = spin_jackpot()

        if jackpot:
            jackpot_count += 1

        records.append({
            "trial": i + 1,
            "slot1": result[0],
            "slot2": result[1],
            "slot3": result[2],
            "jackpot": jackpot
        })

    fail_count = TRIAL_COUNT - jackpot_count
    jackpot_rate = jackpot_count / TRIAL_COUNT

    df = pd.DataFrame(records)

    df.to_csv(
        RESULT_PATH,
        index=False,
        encoding="utf-8-sig"
    )

    mlflow.log_metric("jackpot_count", jackpot_count)
    mlflow.log_metric("fail_count", fail_count)
    mlflow.log_metric("jackpot_rate", jackpot_rate)

    mlflow.log_artifact(RESULT_PATH)

    print(f"Result saved to: {RESULT_PATH}")
    print(f"jackpot_count: {jackpot_count}")
    print(f"fail_count: {fail_count}")
    print(f"jackpot_rate: {jackpot_rate:.4f}")