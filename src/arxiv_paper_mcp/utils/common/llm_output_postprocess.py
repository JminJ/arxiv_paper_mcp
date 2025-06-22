import re


def extract_codeblock_content(llm_output: str) -> str:
    """
    Extract code block content from LLM output.
    Supports ```python, ```text, or just ``` blocks.
    Returns the inner content without code block markers.
    """
    pattern = r"```(?:\w+)?\n(.*?)```"
    match = re.search(pattern, llm_output, re.DOTALL)

    if match:
        return match.group(1).strip()
    else:
        # fallback: no code block found, return original
        return llm_output.strip()
    