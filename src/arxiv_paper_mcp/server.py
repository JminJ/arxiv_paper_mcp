from typing import Dict, List

from fastmcp import FastMCP

from src.arxiv_paper_mcp.utils.arxiv_utils.arxiv_search_utils import (
    ArxivSearchUtils,
)

arxiv_search_utils = ArxivSearchUtils()

mcp_server = FastMCP(
    name="Arxiv paper MCP server",
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