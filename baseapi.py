import json
import os
import hashlib
import glob
from openai import OpenAI
import configparser

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

client = OpenAI(
    api_key = config["Openai"]["api_key"],
    base_url = config["Openai"]["base_url"]    
)

#创建 assistant
def create_assistant(robot_json):
    response = client.beta.assistants.create(
        name = robot_json["assistant_info"]["name"],
        instructions = robot_json["assistant_info"]["instructions"],
        model = robot_json["assistant_info"]["model"]
    )
    assistant_id = response.id
    return assistant_id

# 更新 assistant
def update_assistant(robot_json):
    assistant_id = robot_json["assistant_id"]
    client.beta.assistants.update(
        assistant_id,
        name = robot_json["assistant_info"]["name"],
        instructions = robot_json["assistant_info"]["instructions"],
        model = robot_json["assistant_info"]["model"],
        tools = robot_json["assistant_info"]["tools"],
        tool_resources = robot_json["assistant_info"]["tool_resources"]
    )
    return None

# 创建向量存储获取向量存储 ID
def create_vector_store(robot_json):
    response = client.beta.vector_stores.create(
        name = robot_json["assistant_info"]["name"] + "_vector_store",
    )
    vector_store_id = response.id
    return vector_store_id

# 上传文件获取文件 ID
def upload_file(file_path):
    response = client.files.create(
        file = open(file_path, "rb"),
        purpose = "assistants"
    )
    file_id = response.id
    return file_id

def delete_file(file_id):
    client.files.delete(
        file_id = file_id
    )
    return None

def attach_file_to_vector_store(robot_json):
    vector_store_id = robot_json["assistant_info"]["tool_resources"]["file_search"]["vector_store_ids"][0]
    file_openai_ids = robot_json["attact_file_info"]["file_openai_ids"]

    for file_openai_id in file_openai_ids:
        client.beta.vector_stores.files.create(
            vector_store_id = vector_store_id,
            file_id = file_openai_id
        )
    return None