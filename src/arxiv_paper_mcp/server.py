import os
import traceback
from typing import Dict, List

from fastmcp import FastMCP

from src.arxiv_paper_mcp.utils.arxiv_utils.arxiv_search_utils import (
    ArxivSearchUtils,
)
from src.arxiv_paper_mcp.utils.common.pdf_handling import (
    get_target_paper_pdf_file_path,
    get_target_paper_section_file_path,
)
from src.arxiv_paper_mcp.utils.paper_utils.paper_analysis_utils import (
    analyze_target_paper,
)
from src.arxiv_paper_mcp.utils.paper_utils.paper_download_utils import (
    paper_pdf_download,
)

arxiv_search_utils = ArxivSearchUtils()

mcp_server = FastMCP(
    name="Arxiv Paper MCP Server",
    instructions="Search papers from Arxiv API that user want to search."
)

@mcp_server.tool(
    name="search_papers_based_user_query",
    description="Search papers from Arxiv API that user want to search.",
)
async def search_papers_based_userinput(user_input:str)->List[Dict]:
    """사용자 입력 메세지를 기반으로 arxiv api에서 논문들을 검색 및 정보 반환

    Args:
        user_input (str): user input text. system will generate search query based this text.

    Return:
        List[Dict]: 논문들의 infos.
    """
    search_results = arxiv_search_utils.search_user_want_papers(user_question=user_input)

    return search_results


@mcp_server.tool(
    name="paper_download_tool",
    description="download target paper by given arxiv paper id."
)
async def download_target_paper(paper_id:str)->bool:
    """사용자가 분석/다운로드를 요청한 논문을 arxiv paper id를 통해 다운로드합니다.

    Args:
        paper_id (str): 대상 arxiv paper id

    Return:
        bool
    """
    paper_download_path = get_target_paper_pdf_file_path(paper_id)
    print(paper_download_path)
    if not os.path.exists(paper_download_path):
        try:
            await paper_pdf_download(paper_id)
            return True
        except Exception as E:
            print(traceback.format_exc())
            print(E)
            return False
    else:
        print("해당 논문은 이미 다운로드 되었습니다.")
        return True


@mcp_server.tool(
    name="return_section_names_tool",
    description="return section names of target paper"
)
async def return_paper_section_names(paper_id:str)->str:
    """사용자가 요청한 논문의 섹션명 정보들을 반환합니다.

    Args:
        paper_id (str): 대상 논문의 paper id

    Returns:
        str: 대상 논문의 섹션명 정보
    """
    target_paper_section_name_file_path = get_target_paper_section_file_path(paper_id=paper_id)
    with open(target_paper_section_name_file_path, "r") as f:
        target_paper_section_names = f.readlines()
        
    return target_paper_section_names


@mcp_server.tool(
    name="description_paper_content",
    description="Descrive paper content and section from user question."
)
async def descrive_paper_content(
    paper_id:str,
    section_names:List[str],
    raw_user_question:str
)->str:
    """대상 논문에 대해 사용자가 궁금해하는 내용 또는 섹션을 설명합니다.

    Args:
        paper_id (str): 대상 논문 arxiv id
        section_names (List[str]): 사용자가 설명을 바라는 section들(사용자 원본 질문에서 섹션명들을 추출하세요)
        raw_user_question (str): 사용자의 질문 원본 내용

    Returns:
        str: llm의 설명 내용
    """
    llm_result = await analyze_target_paper(
        paper_id,
        section_names,
        raw_user_question
    )

    return llm_result
    