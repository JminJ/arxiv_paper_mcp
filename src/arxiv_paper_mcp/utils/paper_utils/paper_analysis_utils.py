from typing import List

from src.arxiv_paper_mcp.llm.chains import paper_description_chain
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

        