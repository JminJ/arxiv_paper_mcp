from langchain.chat_models import init_chat_model

from src.arxiv_paper_mcp.config.global_resources import (
    MODEL_SEED,
    MODEL_TEMPERATURE,
    USING_MODEL_INFO,
)

LLM_MODEL = init_chat_model(
    USING_MODEL_INFO, 
    temperature=MODEL_TEMPERATURE, 
    generation_config={
        "seed": MODEL_SEED
    }
)