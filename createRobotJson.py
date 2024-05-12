robot = {
    "assistant_info": {
        "name": "",
        "instructions": "",
        "model": "",
        "tools": [
            {
                "type": "file_search"
            }
        ],
        "tool_resources": {
            "file_search": {
                "vector_store_ids": [
                ]
            }
        }
    },
    "assistant_md5": "",
    "assistant_id": "",
    "attact_file_info": {
        "file_paths": [
        ],
        "file_md5s": [
        ],
        "file_openai_ids": [
        ]
    }
}

def create():
    robot["assistant_info"]["name"] = input("请输入机器人名称：") or "assistant_name"
    robot["assistant_info"]["instructions"] = input("请输入机器人指令：") or "你是一个智能助手。"
    robot["assistant_info"]["model"] = input("请输入机器人模型：") or "gpt-3.5-turbo"
    print(robot)
    return robot

