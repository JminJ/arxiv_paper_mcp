import os

from dotenv import find_dotenv, load_dotenv

from src.arxiv_paper_mcp.utils.common.common_utils import get_workspace_path

load_dotenv(find_dotenv())


USING_MODEL_INFO=os.getenv("USING_MODEL_INFO")
MODEL_TEMPERATURE=0.0 # 고정
MODEL_SEED=256 # 고정


PDF_DOWNLOAD_PATH=f"{get_workspace_path()}/src/arxiv_paper_mcp/data/paper_pdf" # 고정
PDF_SECTION_SAVE_PATH=f"{get_workspace_path()}/src/arxiv_paper_mcp/data/paper_sections" # 고정