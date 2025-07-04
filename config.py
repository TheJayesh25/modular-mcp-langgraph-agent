
import os
from pathlib import Path
from dotenv import load_dotenv
import json

load_dotenv()

def resolve_env_vars(config: dict) -> dict:
    for server_name, server_config in config.items():
        if "env" in server_config:
            for key, value in server_config["env"].items():
                if isinstance(value, str) and value.startswith("${"):
                    env_var_name = value[2:-1]
                    env_value = os.environ.get(env_var_name)
                    if env_value is None:
                        raise ValueError(f"Environment variable {env_var_name} not set")
                    config[server_name]["env"][key] = env_value
        if "args" in server_config:
            for i, arg in enumerate(server_config["args"]):
                if isinstance(arg, str) and arg.startswith("${"):
                    env_var_name = arg[2:-1]
                    env_value = os.environ.get(env_var_name)
                    if env_value is None:
                        raise ValueError(f"Environment variable {env_var_name} not set")
                    config[server_name]["args"][i] = env_value
    return config

config_file = Path(__file__).parent / "mcp_config.json"
if not config_file.exists():
    raise FileNotFoundError(f"Missing mcp_config.json at {config_file}")

with open(config_file) as f:
    raw_config = json.load(f)

mcp_config = resolve_env_vars(raw_config)
