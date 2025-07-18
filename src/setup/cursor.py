import json
import os
from pathlib import Path
from typing import Dict, List


def get_cursor_mcp_config_path() -> Path | None:
    """Get the Cursor MCP config directory based on platform."""
    path = Path(Path.home(), ".cursor")
    if path.exists():
        return path
    return None


def get_workspace_path() -> Path:
    """Return path of workspace.

    Returns:
        Path: directory path of workspace
    """
    workspace_path = Path(__file__).parent.parent.parent
    return workspace_path


def write_mcp_json_file(mcp_file_path:str, mcp_file_dict:Dict):
    """Generate or Update mcp.json file

    Args:
        mcp_file_path (str): mcp file path
        mcp_file_dict (Dict): mcp file dict
    """
    with open(mcp_file_path, "w", encoding="utf-8") as mcp_json_file:
        json.dump(mcp_file_dict, mcp_json_file, indent="\t")
        

def check_env_dict(env_dict:Dict[str, str]):
    """Check if dict has required values ​​or not

    Args:
        env_dict (Dict[str, str]): env dict obj
    """
    assert "GOOGLE_API_KEY" in env_dict, "Missing GOOGLE_API_KEY in env."
    assert "USING_MODEL_INFO" in env_dict, "Missing USING_MODEL_INFO in env."


def setting_mcp_json(server_name:str, env_vars: Dict[str, str]):
    """setting mcp.json file

    Args:
        server_name (str): mcp server name
        env_vars (Dict[str, str]): env dict object
    """
    # 1. check path os .cursor directory 
    cursor_config_dir = get_cursor_mcp_config_path()     
    if not cursor_config_dir:
        raise RuntimeError(
            "Cursor config directory not found. Please ensure Cursor "
            "is installed and has been run at least once to initialize its configuration."
        )

    cursor_config_file_path = os.path.join(cursor_config_dir, "mcp.json")

    if not os.path.exists(cursor_config_file_path):
        write_mcp_json_file(cursor_config_file_path, {}) # 파일이 존재하지 않을 시, 생성
    
    with open(cursor_config_file_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    if "mcpServers" not in config:
        config["mcpServers"] = {}

    # Always preserve existing env vars and merge with new ones
    if (
        server_name in config["mcpServers"]
        and "env" in config["mcpServers"][server_name]
    ):
        existing_env = config["mcpServers"][server_name]["env"]
        if env_vars:
            # New vars take precedence over existing ones
            env_vars = {**existing_env, **env_vars}
        else:
            env_vars = existing_env

    # Build run command
    args = ["-m", "src.arxiv_paper_mcp.server"]

    server_config = {
        "command": "python",
        "args": args,
    }

    # Add environment variables if specified
    workspace_path = str(get_workspace_path())
    env_vars["PYTHONPATH"] = workspace_path # add PYTHONPATH
    env_vars["PATH"] = os.path.join(workspace_path, ".venv", "bin")+":${PATH}"# add PATH
    server_config["env"] = env_vars

    # CHECK env_vars
    check_env_dict(env_dict=server_config["env"])

    config["mcpServers"][server_name] = server_config

    # UPDATE json file
    write_mcp_json_file(mcp_file_path=cursor_config_file_path, mcp_file_dict=config)
    
 
def _make_env_dict(raw_env_vars: List[str]):
    env_dict = {}

    for env_var in raw_env_vars:
        key, value = env_var.split("=", 1)
        env_dict[key.strip()] = value.strip()

    return env_dict


def install_to_cursor(env_vars: List[str]):
    """Install MCP server to Cursor.

    Args:
        env_vars (List[str]): 
    """
    mcp_server_name = "Arxiv Paper MCP Server"
    env_dict = _make_env_dict(env_vars)
    setting_mcp_json(server_name=mcp_server_name, env_vars=env_dict)

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "--env",
        "-e",
        action="append",
        help="ENV args to set for the server."
    )

    args = parser.parse_args()

    install_to_cursor(
        env_vars=args.env
    )