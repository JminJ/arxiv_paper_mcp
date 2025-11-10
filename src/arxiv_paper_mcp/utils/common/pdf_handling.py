import os
from typing import Dict, List

from PyPDF2 import PdfReader

from src.arxiv_paper_mcp.config.global_resources import (
    PDF_DOWNLOAD_PATH,
    PDF_SECTION_SAVE_PATH,
)


def extract_all_text_each_page(target_pdf_reader: PdfReader)->Dict[int, str]:
    """단일 페이지를 기준으로 text를 추출

    Args:
        target_pdf_reader (PdfReader): 추출 대상 pdf reader object

    Returns:
        Dict[int, str]: page number, page text content format dictionary
    """
    each_page_dict = {}

    for page_number, page in enumerate(target_pdf_reader.pages, 0):
        each_page_dict[page_number] = page.extract_text()

    return each_page_dict


def get_target_paper_section_dir_path(paper_id:str)->str:
    """논문 id 기반으로 목차 디렉토리 경로를 반환합니다.

    Args:
        paper_id (str): 대상 논문 paper id

    Returns:
        str: 목차 파일 경로
    """
    return os.path.join(PDF_SECTION_SAVE_PATH, paper_id)


def get_target_paper_section_file_path(paper_id:str)->str:
    """논문 id 기반으로 목차 파일 경로를 반환합니다.

    Args:
        paper_id (str): 대상 논문 paper id

    Returns:
        str: 목차 파일 경로
    """
    temp_paper_pdf_directory_path = get_target_paper_section_dir_path(paper_id)
    return os.path.join(temp_paper_pdf_directory_path, "sections_info.txt")


def get_papers_section_list(paper_ids:List[str])->Dict[str, List]:
    """대상 논문들의 목차 값들을 반환

    Args:
        paper_ids (List[str]): 대상 논문 arxiv id들. 

    Returns:
        Dict[str]: 논문 별 목차 정보 dict.
    """
    paper_sections = {}
    for paper_id in paper_ids:
        temp_paper_path = get_target_paper_section_file_path(paper_id)
        with open(temp_paper_path, "r") as f:
            v = eval(f.readline())
            paper_sections[paper_id] = v

    return paper_sections

        
def get_target_paper_pdf_file_path(paper_id:str)->str:
    """논문 id를 기반으로 pdf파일 경로를 반환합니다.

    Args:
        paper_id (str): 대상 논문 id

    Returns:
        str: 저장된 pdf 파일 경로
    """
    return os.path.join(PDF_DOWNLOAD_PATH, f"{paper_id}.pdf")


def extract_target_page_contents(paper_id: str, target_page_numbers:List[int])->List[str]:
    """대상 페이지 번호에 대한 페이지 내용들을 추출, 반환

    Args:
        paper_id (str): 대상 논문 arxiv id
        target_page_numbers (List[int]): 대상 페이지 번호 리스트

    Returns:
        List[str]: 대상 페이지 추출한 내용 리스트
    """
    page_content_list = []

    paper_path = get_target_paper_pdf_file_path(paper_id) # 대상 논문 pdf 파일 경로 반환
    paper_loader = PdfReader(paper_path)

    for page_number in target_page_numbers:
        page_content_list.append(paper_loader.pages[page_number].extract_text())

    return page_content_list


if __name__ == "__main__":
    # result = extract_target_page_contents(paper_id="2505.13006", target_page_numbers=[0,1])
    # result = get_target_paper_pdf_file_path(paper_id="2505.13006")
    result = get_papers_section_list(
        paper_ids=[
            "1706.03762",
        ]
    )
    print(result)