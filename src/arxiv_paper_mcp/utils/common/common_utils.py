import os
from pathlib import Path


def get_workspace_path():
    dir_path = Path(__file__).resolve().parent.parent.parent.parent.parent # HACK
    return dir_path

def check_directory(target_path:str)->bool:
    """디렉토리가 존재하는지 bool 리턴
    """
    return os.path.exists(target_path)

def mkdir_directory(target_path:str):
    """대상 디렉토리 경로 생성
    """
    path = Path(target_path)
    path.mkdir(parents=True, exist_ok=True)

def extract_paper_id_from_path(paper_pdf_file_path:str)->str:
    """논문 pdf 파일 경로에서 arxiv paper id를 추출

    Args:
        paper_pdf_file_path (str): 대상 논문 pdf 파일 경로

    Returns:
        str: 추출된 arxiv paper id
    """
    paper_file_name = paper_pdf_file_path.split("/")[-1]
    arxiv_paper_id = ".".join(paper_file_name.split(".")[:-1]) # 파일 이름 내 '.'가 존재할 수 있기 때문에

    return arxiv_paper_id

if __name__ == "__main__":
    path = get_workspace_path()
    print(path)