import os

USING_MODEL_INFO=os.getenv("USING_MODEL_INFO")
MODEL_TEMPERATURE=float(os.getenv("MODEL_TEMPERATURE", "0.0"))
MODEL_SEED=int(os.getenv("MODEL_SEED", "256"))