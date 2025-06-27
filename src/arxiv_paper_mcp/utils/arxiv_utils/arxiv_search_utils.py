import urllib
import urllib.request
from typing import Dict, List

import feedparser

from src.arxiv_paper_mcp.llm_chains.chains import arxiv_search_query_generation_chain
from src.arxiv_paper_mcp.utils.common.llm_output_postprocess import (
    extract_codeblock_content,
)


class ArxivSearchUtils:
    def __init__(self):
        self.arxiv_api_url_template = "http://export.arxiv.org/api/query?search_query={search_query}"


    def _url_open(self, url:str):
        return urllib.request.urlopen(url)


    def _extract_using_values_from_entry(self, raw_entry)->Dict[str, str]:
        """entry 내에서 사용될 값만 추출
            - title
            - author
            - tags
            - paper_id
            - summary

        Args:
            raw_entry: 원본 entry, 해당 값에서 사용될 내용만을 추출. 
        """
        using_value = {}

        using_value["title"] = raw_entry["title"].strip()
        using_value["authors"] = ", ".join([author["name"].strip() for author in raw_entry["authors"]])
        using_value["tags"] = str(", ".join([tag["term"].strip() for tag in raw_entry["tags"]]))
        paper_id = str(raw_entry["link"].split("/")[-1][:10])
        using_value["paper_id"] = paper_id
        using_value["summary"] = raw_entry["summary"]

        return using_value


    def request_arxiv_api_by_search_query(self, search_query:str):
        """search_query를 기반으로 arxiv api에서 논문들을 조회합니다.

        Args:
            search_query (str): search_query.
        """
        
        # url open & rss feed get
        response = self._url_open(self.arxiv_api_url_template.format(search_query=search_query))
        rss_feed = response.read()

        # rss_feed parse
        feed_parsing_result = feedparser.parse(rss_feed).entries
        extracted_using_value_result = [self._extract_using_values_from_entry(parsing_result) for parsing_result in feed_parsing_result]
        
        return extracted_using_value_result
        

    def search_user_want_papers(self, user_question:str)->List[Dict[str, str]]:
        """사용자 입력 기반 arxiv 논문 검색 수행, 결과를 반환합니다.

        Args:
            user_question (str): 사용자 질문 메세지.

        Returns:
            Dict: 결과
        """
        # 1. LLM 기반 arxiv api search query 생성
        search_query = extract_codeblock_content(arxiv_search_query_generation_chain.invoke(
            input={
                "user_question": user_question
            }
        ))
        print(search_query)
        # 2. arxiv api 검색 결과 반환
        searched_paper_infos = self.request_arxiv_api_by_search_query(search_query=search_query)
        return searched_paper_infos
        

if __name__ == "__main__":
    from icecream import ic

    arxiv_search_utils = ArxivSearchUtils()
    search_reuslt = arxiv_search_utils.search_user_want_papers(
        user_question="자연어처리 논문 중 RAG 관련 논문을 검색해주세요"
    )
    ic(search_reuslt)