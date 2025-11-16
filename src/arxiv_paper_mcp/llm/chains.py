from typing import List, Tuple

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSerializable

from src.arxiv_paper_mcp.llm.llm_define import LLM_MODEL
from src.arxiv_paper_mcp.llm.prompts import ARXIV_PROMPTS, PAPER_PROMPTS


def define_chat_prompt_chain(using_prompt:List[Tuple], llm_model)->RunnableSerializable:
    """chat templage prompt chain 설정하는 base 함수

    Args:
        using_prompt (str): chain에 사용될 chat template 프롬프트
        llm_model: chain에 사용될 LLM model object.

    Returns:
        RunnableSerializable: chain.
    """
    chat_prompt = ChatPromptTemplate.from_messages(
        using_prompt
    )
    chain = chat_prompt | llm_model | StrOutputParser()

    return chain


## define chains
arxiv_search_query_generation_chain = define_chat_prompt_chain(
    using_prompt=ARXIV_PROMPTS["ARXIV_SEARCH_QUERY_GENERATION"],
    llm_model=LLM_MODEL
)

paper_section_extract_chain = define_chat_prompt_chain(
    using_prompt=PAPER_PROMPTS["PAPER_SECTION_QUERY_GENERATION"],
    llm_model=LLM_MODEL
)

paper_description_chain = define_chat_prompt_chain(
    using_prompt=PAPER_PROMPTS["PAPER_ANALYSIS_GENERATION_PROMPT"],
    llm_model=LLM_MODEL
)

paper_target_section_select_chain = define_chat_prompt_chain(
    using_prompt=PAPER_PROMPTS["PAPER_TARGET_SECTION_SELECT_PROMPT"],
    llm_model=LLM_MODEL
)

paper_using_section_select_chain = define_chat_prompt_chain(
    using_prompt=PAPER_PROMPTS["PAPER_USING_SECTION_SELECT_PROMPT"],
    llm_model=LLM_MODEL
)