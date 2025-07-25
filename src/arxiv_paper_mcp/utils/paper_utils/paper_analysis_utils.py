from typing import Dict, List

from src.arxiv_paper_mcp.llm.chains import paper_description_chain
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
    section_contents = await return_target_section_pages(
        paper_id,
        section_names,
        user_question=raw_user_question
    )
    paper_analysis_result = await paper_description_chain.ainvoke(
        input={
            "user_question": raw_user_question,
            "paper_content": section_contents
        }
    )

    return paper_analysis_result


if __name__ == "__main__":
    import asyncio

    from icecream import ic

    result = asyncio.run(
        analyze_target_paper(
            paper_id="2505.13006",
            section_names=[""],
            raw_user_question="논문에서 제시하는 Knowledge Graph 기반 RAG (Graph RAG) 기법에 대해 설명해주세요"
        )
    )

    ic(result)

        