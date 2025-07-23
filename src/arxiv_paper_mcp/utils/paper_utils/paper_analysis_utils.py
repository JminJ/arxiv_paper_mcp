from typing import Dict, List

from src.arxiv_paper_mcp.llm.chains import paper_description_chain
from src.arxiv_paper_mcp.utils.common.common_utils import (
    get_target_paper_section_file_path,
)
from src.arxiv_paper_mcp.utils.paper_utils.paper_download_utils import (
    paper_download_utils,
)
from src.arxiv_paper_mcp.utils.paper_utils.paper_section_utils import (
    paper_section_extract_utils,
    return_target_section_pages,
)


async def analyze_target_paper(paper_id:str, section_names:List[str], raw_user_question:str)->str:
    """대상 논문의 내용을 설명

    Args:
        paper_id (str): 대상 논문의 arxiv id.
        section_names (List[str]): 사용자가 설명받기를 원하는 섹션 명
        raw_user_question (str): 사용자 질문 원문

    Returns:
        str: 설명 결과 텍스트
    """
    section_contents = return_target_section_pages(
        paper_id,
        section_names,
        user_question=raw_user_question
    )
    paper_analysis_result = await paper_description_chain.ainvoke(
        input={
            "user_question": raw_user_question,
            "paper_sections": section_contents
        }
    )

    return paper_analysis_result




        