import os
from pathlib import Path

import wget

from src.arxiv_paper_mcp.config.global_resources import PDF_DOWNLOAD_PATH
from src.arxiv_paper_mcp.utils.common.common_utils import (
    check_directory,
    mkdir_directory,
)


def paper_pdf_download(paper_id:str):
    """논문 pdf 파일을 다운로드합니다.

    Args:
        paper_id (str): 다운로드 대상 paper id.
        pdf_download_path (str): pdf 파일 저장 경로.
    """
    pdf_file_name = f"{paper_id}.pdf"
    http_pdf_url_format = f"https://arxiv.org/pdf/{pdf_file_name}"
    pdf_download_path = os.path.join(str(PDF_DOWNLOAD_PATH), pdf_file_name)
    if not check_directory(PDF_DOWNLOAD_PATH): # 상위 디렉토리 체크 및 생성
        mkdir_directory(PDF_DOWNLOAD_PATH)
    wget.download(http_pdf_url_format, pdf_download_path)


if __name__ == "__main__":
    paper_id = "2505.13006"
    paper_pdf_download(
        paper_id,
    )