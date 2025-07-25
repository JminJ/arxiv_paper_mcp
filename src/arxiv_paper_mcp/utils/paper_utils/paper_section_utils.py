import ast
import asyncio
import os
from typing import Dict, List, Tuple

from icecream import ic
from PyPDF2 import PdfReader

from src.arxiv_paper_mcp.config.global_resources import PDF_SECTION_SAVE_PATH
from src.arxiv_paper_mcp.llm.chains import (
    paper_section_extract_chain,
    paper_target_section_select_chain,
)
from src.arxiv_paper_mcp.utils.common.common_utils import (
    check_directory,
    extract_paper_id_from_path,
    mkdir_directory,
)
from src.arxiv_paper_mcp.utils.common.llm_output_postprocess import (
    extract_codeblock_content,
)
from src.arxiv_paper_mcp.utils.common.pdf_handling import (
    extract_all_text_each_page,
    extract_target_page_contents,
    get_target_paper_section_dir_path,
    get_target_paper_section_file_path,
)


class PaperSectionExtractUtils:
    def __init__(self):
        self.paper_section_extract_chain = paper_section_extract_chain

    async def section_extract_func(self, page_number:int, full_text_content:str)->Tuple[int, List[str]]:
        """논문 페이지 내용에서 목차들을 추출 및 반환

        Args:
            page_number (int): 페이지 번호
            full_text_content (str): 해당 페이지 텍스트 내용

        Returns:
            Tuple[int, List[str]]: (페이지 번호, 추출된 목차들 list) 형태의 튜플 반환.
        """
        extracted_section_raw_text = await self.paper_section_extract_chain.ainvoke(
            input={
                "paper_page_content": full_text_content
            }
        )

        extracted_sections = ast.literal_eval(extract_codeblock_content(extracted_section_raw_text))
        return (page_number, extracted_sections)

    def __each_page_section_organize(self, each_page_extract_result:List[Tuple[int, List[str]]])->Dict[str, List[int]]:
        """각 페이지마다 목차값들을 정리

        Args:
            each_page_extract_result (List[Tuple[int, List[str]]]): 각 페이지마다 추출된 목차 값들

        Returns:
            Dict[str, List[int]]: 목차마다 해당되는 페이지 번호 리스트 가진 Dict
        """
        each_sections_page_info_dict = {}
        for result_idx in range(len(each_page_extract_result)):
            result = each_page_extract_result[result_idx]
            temp_page_number = result[0]
            temp_page_sections = result[1]

            for section in temp_page_sections: # 페이지 내 목차 순회
                each_sections_page_info_dict[section] = [temp_page_number]
                if section == temp_page_sections[-1]: # 현재 목차가 해당 페이지의 마지막 목차일 시
                    if result_idx == len(each_page_extract_result)-1: # 만약 현재 페이지가 논문의 마지막 페이지였을 경우
                        continue
                    next_section_page_number = each_page_extract_result[result_idx+1][0]
                    each_sections_page_info_dict[section].extend(range(temp_page_number+1, next_section_page_number+1)) # 현재 페이지 번호+1 ~ 다음 페이지 번호+1 까지 추가
        
        return each_sections_page_info_dict

    def __save_section_infos(self, paper_pdf_path:str, paper_sections:Dict[str, List[int]]):
        """추출된 목차 정보를 txt파일로 저장

        Args:
            paper_pdf_path (str): 추출 대상 pdf파일의 저장 경로
            paper_sections (Dict[str, List[int]]): 추출된 목차 정보
        """
        if not check_directory(PDF_SECTION_SAVE_PATH): # 목차 저장 디렉토리 존재 유무 체크 및 없을 시 생성
            mkdir_directory(PDF_SECTION_SAVE_PATH)
        
        # 1. 현재 pdf 목차 저장 디렉토리 생성
        paper_pdf_name = extract_paper_id_from_path(paper_pdf_path)
        temp_paper_pdf_directory_path = get_target_paper_section_dir_path(paper_pdf_name)
        mkdir_directory(temp_paper_pdf_directory_path)

        # 2. 목차 txt파일 저장
        with open(str(os.path.join(temp_paper_pdf_directory_path, "sections_info.txt")), "w") as serction_info_file:
            serction_info_file.write(f"{paper_sections}")

    async def page_section_extract(self, each_page_text_dict:Dict[int, str])->Dict[str, List[int]]:
        """페이지마다 목차를 추출, 목차마다 어느 페이지에 존재하는지 결과를 반환

        Args:
            each_page_text_dict (Dict[int, str]): 페이지에 대한 텍스트 추출 결과 내용

        Returns:
            Dict[str, List[int]]: 목차에 대해 어느 페이지 내에 해당 목차가 존재하는지 반환
        """
        # 1. 비동기로 페이지마다 목차 추출
        corutines = []
        for page_number in each_page_text_dict.keys():
            temp_page_content = each_page_text_dict[page_number]
            corutines.append(self.section_extract_func(page_number, temp_page_content))
        corutine_results = await asyncio.gather(*corutines)
        ic(corutine_results)

        # 2. 추출된 결과 기반 Dict[str, List[int]] 포맷으로 가공
        each_page_section_dict = self.__each_page_section_organize(corutine_results)

        return each_page_section_dict

    async def extract_sections_main(self, pdf_file_path:str):
        """논문 pdf 내에서 목차 정보를 해당되는 페이지 번호들과 함께 Dict로 추출, 저장

        Args:
            pdf_file_path (str): 대상 논문 pdf 파일 경로
        """
        # 1. 논문 pdf 로드
        target_pdf_reader = PdfReader(pdf_file_path)
        each_page_texts = extract_all_text_each_page(target_pdf_reader)
        
        # 2. 목차 별 페이지 정보 반환
        each_sections_page_number_info = await self.page_section_extract(each_page_text_dict=each_page_texts)

        # 3. 목차 정보 파일 저장
        self.__save_section_infos(pdf_file_path, each_sections_page_number_info)


paper_section_extract_utils = PaperSectionExtractUtils()


def load_paper_section_infos(paper_id:str)->Dict[str, List[int]]:
    """논문 섹션 정보를 읽어와 str으로 반환

    Args:
        paper_id (str): 대상 논문 paper id

    Returns:
        Dict[str, List[int]]: 섹션, 페이지 정보 dict 
    """
    section_file_path = get_target_paper_section_file_path(paper_id)

    with open(section_file_path, "r") as f:
        section_infos = f.readlines()

    return ast.literal_eval(section_infos[0]) # 단일 라인으로 저장되므로


async def get_section_names_by_llm(user_question:str, paper_section_infos:Dict[str, List[int]])->List[str]:
    """llm chain을 통해 사용자 입력에서 대상 섹션명을 추출

    Args:
        user_question (str): 사용자 입력 질문 내용
        paper_section_infos (Dict[str, List[int]]): 대상 논문의 섹션 정보

    Returns:
        List[str]: 추출된 섹션명 리스트
    """
    extracted_section_names = await paper_target_section_select_chain.ainvoke(
        input={
            "user_question": user_question,
            "paper_sections": paper_section_infos
        }
    )   
    extracted_section_names = ast.literal_eval(extract_codeblock_content(extracted_section_names))
    
    return extracted_section_names


def return_target_section_pages(paper_id:str, section_names:List[str], user_question:str)->List[str]:
    """대상 섹션 페이지 내용을 반환합니다.

    Args:
        paper_id (str): 대상 논문 arxiv id
        section_names (List[str]): 추출한 섹션명들
        user_question (str): 사용자 질문 내용

    Returns:
        List[str]: 대상 섹션에 대한 페이지 내용
    """
    def need_or_not_llm_check(section_names:List[str], paper_section_infos:Dict[str, List[int]])->bool:
        """section 명들에 대해 llm 기반 분석이 필요한지 체크합니다.
        
        Args:
            section_names (List[str]): 사용자 입력 section 명들

        Returns:
            bool: llm 분석이 필요한지 여부
        """
        need_llm_checks = []
        for section_name in section_names:
            if section_name not in list(paper_section_infos.keys()):
                need_llm_checks.append(True)
            else:
                need_llm_checks.append(False)

        return all(need_llm_checks)

    # 1. 대상 논문의 섹션 정보를 추출
    target_paper_sections = load_paper_section_infos(paper_id)

    # 2. 사용할 섹션이 있는 페이지 번호들을 추출
    using_page_numbers = []
    need_llm_check_result = need_or_not_llm_check(section_names, target_paper_sections) # llm 기반 섹션명 검색이 필요한지 아닌지 체크
    if need_llm_check_result: 
        section_names = get_section_names_by_llm(user_question, paper_section_infos=target_paper_sections)
    for section_name in section_names:
        section_page_numbers = target_paper_sections[section_name]
        using_page_numbers.extend(section_page_numbers)
        
    # 3. 페이지 텍스트 추출 및 반환
    page_text_contents = extract_target_page_contents(paper_id=paper_id, target_page_numbers=using_page_numbers)
    return page_text_contents


if __name__ == "__main__":
    import asyncio

    from icecream import ic

    reuslt = asyncio.run(paper_section_extract_utils.extract_sections_main(
        pdf_file_path="/workspaces/arxiv_paper_mcp/src/arxiv_paper_mcp/data/paper_pdf/2505.13006.pdf"
    ))
    ic(result)
    