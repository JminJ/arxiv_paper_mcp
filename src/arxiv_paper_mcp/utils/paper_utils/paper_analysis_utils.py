import ast
from typing import List

from src.arxiv_paper_mcp.llm.chains import (
    paper_description_chain,
    paper_using_section_select_chain,
)
from src.arxiv_paper_mcp.utils.common.llm_output_postprocess import (
    extract_codeblock_content,
)
from src.arxiv_paper_mcp.utils.common.pdf_handling import (
    get_papers_section_list,
)
from src.arxiv_paper_mcp.utils.paper_utils.paper_section_utils import (
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


async def analyze_multi_papers(paper_ids:List[str], raw_user_quesiton:str)->str:
    """사용자의 요구에 맞추어 여러 논문들의 내용을 설명

    Args:
        paper_ids (List[str]): 대상 논문 arxiv id들. 
        raw_user_quesiton (str): 사용자 질문 원문

    Returns:
        str: 설명 결과 텍스트
    """
    # 1. 논문들의 섹션 리스트 추출
    paper_sections = get_papers_section_list(paper_ids)

    # 2. 사용자 질문에 대해 논문들마다 사용되어야 할 섹션 선정
    using_section_names = await paper_using_section_select_chain.ainvoke(
        input={
            "raw_question": raw_user_quesiton,
            "paper_section_infos": paper_sections
        }
    )
    using_section_names = ast.literal_eval(extract_codeblock_content(using_section_names))
    
    # 3. 선정 섹션에 대해 페이지 내용 가져오기
    using_paper_conts = {}
    for paper_id, section_names in using_section_names.items():
        temp_paper_content = await return_target_section_pages(
            paper_id,
            section_names
        )
        using_paper_conts[paper_id] = temp_paper_content
    
    # 4. 논문 내용 기반 질문 답변 생성
    gen_result = await paper_description_chain.ainvoke(
        input={
            "user_question": raw_user_quesiton,
            "paper_content": using_paper_conts
        }
    )

    return gen_result


if __name__ == "__main__":
    import asyncio

    from icecream import ic

    result = asyncio.run(
        analyze_target_paper(
            paper_id="2507.10524",
            section_names=[
                "3. Experiments",
                "3.1. Main Results",
                "3.2. IsoFLOP Analysis",
                "3.3. Inference Throughput Evaluation",
                "4. Ablation Studies",
                "4.1. Parameter Sharing Strategies",
                "4.2. Routing Strategies",
                "4.3. KV Caching Strategies",
                "5. Analysis",
                "5.1. Compute-optimal Scaling Analysis",
                "5.2. Routing Analysis",
                "5.3. Test-time Scaling Analysis",
                "6. Related Work",
                "Adaptive computation.",
                "Routing mechanism.",
                "Key-value caching.",
                "Latent reasoning."
            ],
            raw_user_question="각 목차(3. Experiments, 4. Ablation Studies, 5. Analysis, 6. Related Work)와 그 하위 세부 섹션들의 내용을 모두 설명해줘."
        )
    )

    ic(result)

        