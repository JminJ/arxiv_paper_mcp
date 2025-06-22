from typing import List, Tuple

from langchain.chat_models.base import _ConfigurableModel
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSerializable

from src.arxiv_paper_mcp.llm_chains.llm_define import LLM_MODEL
from src.arxiv_paper_mcp.llm_chains.prompts import ARXIV_PROMPTS


def define_chat_prompt_chain(using_prompt:List[Tuple], llm_model:_ConfigurableModel)->RunnableSerializable:
    """chat templage prompt chain 설정하는 base 함수

    Args:
        using_prompt (str): chain에 사용될 chat template 프롬프트
        llm_model (_ConfigurableModel): chain에 사용될 LLM model object.

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