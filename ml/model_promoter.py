import mlflow
from mlflow.tracking import MlflowClient

from app.config import REGISTERED_MODEL_NAME


def get_champion_jackpot_rate(client: MlflowClient) -> float:
    try:
        champion = client.get_model_version_by_alias(
            REGISTERED_MODEL_NAME,
            "champion"
        )

        champion_run = client.get_run(champion.run_id)

        return champion_run.data.metrics.get(
            "jackpot_rate",
            -1.0
        )

    except Exception:
        return -1.0


def promote_if_better(new_version: str, new_jackpot_rate: float):
    client = MlflowClient()

    current_rate = get_champion_jackpot_rate(client)

    print(f"[PROMOTION] current champion jackpot_rate = {current_rate}")
    print(f"[PROMOTION] new candidate jackpot_rate = {new_jackpot_rate}")

    if new_jackpot_rate > current_rate:
        client.set_registered_model_alias(
            name=REGISTERED_MODEL_NAME,
            alias="champion",
            version=str(new_version)
        )

        print(f"[PROMOTION] version {new_version} promoted to champion")

    else:
        print("[PROMOTION] champion unchanged")