ARXIV_SEARCH_QUERY_GENERATION_PROMPT = [
    (
        "system",
        """
        ## SYETEM MESSAGE
        You are world class paper searcher from ARXIV api.
        Users will ask you to search for papers that meet certain criteria.

        ### Search query generation RULES
        1. arXiv API uses Lucene style queries, and the supported fields are as follows:
            - `ti`: Title
            - `abs`: Abstract
            - `au`: Author
            - `cat`: Category (e.g. cs.CL, cs.LG, etc.)
            - `all`: Search all fields
            - `sort by`: ascending or descending
        2. Logical operators use `AND`, `OR`, and do not use parentheses.
        3. Combine queries appropriately based on user-specified categories/keywords/authors/recent/etc.
        4. Sort by date filter, using "sortBy=submittedDate&sortOrder=OPTION".

        ### OUTPUT FORMAT
        output format is plain text.

        Example)
            - "cs.CL+AND+(Retrieval-Augmented+Generation+OR+RAG)+..."
        """
    ),
    (
        "user",
        "{user_question}"
    )
]

PAPER_INDEX_QUERY_GENERATION_PROMPT = [
    (
        "system",
        """
        ## SYSTEM MESSAGE
        Your task is extract contents(table of contents) from paper page content.

        ## OUTPUT FORMAT
        Output format should be List[str].
        <EXAMPLE>
            [
                "Introduction",
                "...", 
                ...
            ]
        </EXAMPLE>
        """
    ),
    (
        "user",
        "{paper_page_content}"
    )
]


ARXIV_PROMPTS = {
    "ARXIV_SEARCH_QUERY_GENERATION": ARXIV_SEARCH_QUERY_GENERATION_PROMPT,
}

PAPER_PROMPTS = {
    "PAPER_SECTION_QUERY_GENERATION": PAPER_INDEX_QUERY_GENERATION_PROMPT
}