from typing import Dict

from PyPDF2 import PdfReader

# def open_pdf_file(target_pdf_path:str)->PdfReader:
#     """대상 pdf파일의 PdfReader를 반환

#     Args:
#         target_pdf_path (str): 대상 pdf파일

#     Returns:
#         PdfReader
#     """
#     target_pdf_reader = PdfReader(target_pdf_path)

#     return target_pdf_reader


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