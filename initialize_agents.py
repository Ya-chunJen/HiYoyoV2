import json,sys,os
import glob
import baseapi
import getmd5
import createRobotJson

workdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(workdir)


#初始化 assistant
def format_assistant(robot_name):
    robot_dir = os.path.join(workdir,'agents', robot_name)
    robot_json_path = os.path.join(robot_dir, 'robot.json')

    if os.path.exists(robot_json_path):
        # print("File path exists.")
        with open(robot_json_path, 'r') as f:
            robot = json.load(f)
    else:
        # print("File path does not exist.")
        robot = createRobotJson.create()

    assistant_info = robot["assistant_info"]
    vector_store_ids = assistant_info['tool_resources']['file_search']['vector_store_ids']

    # 判断vector_store_ids的长度如果是 0 ，就创建一个vector_store_id
    if len(vector_store_ids) == 0:
        robot['assistant_info']['tool_resources']['file_search']['vector_store_ids'].append(baseapi.create_vector_store(robot))

    # 判断字典 robot 中是否包含 assistant_md5 这个 key，并且其值是否为空，就计算assistant_info的md5值
    if 'assistant_md5' not in robot or not robot['assistant_md5']:
        robot['assistant_md5'] = getmd5.json2md5(assistant_info)
    
    # 判断字典 robot 中是否包含 assistant_id 这个 key，并且其值是否为空，就创建一个assistant_id
    if 'assistant_id' not in robot or not robot['assistant_id']:
        robot['assistant_id'] = baseapi.create_assistant(robot)

    # 判断字典robot中attact_file_info中file_paths的长度是为0，如果是0 就要初始化创建向量数据库，并将文件上传到向量数据库中
    if len(robot["attact_file_info"]['file_paths']) == 0:
        for file_path in glob.glob(os.path.join(robot_dir, "*.txt")):
            robot["attact_file_info"]['file_paths'].append(file_path)
        
        for file_path in robot["attact_file_info"]['file_paths']:
            robot["attact_file_info"]['file_md5s'].append(getmd5.file2md5(file_path))
            robot["attact_file_info"]['file_openai_ids'].append(baseapi.upload_file(file_path))
        
        baseapi.attach_file_to_vector_store(robot)

    # 写入robots.json文件
    with open(robot_json_path, 'w', encoding='utf-8') as f:
        json.dump(robot, f, indent=4 ,ensure_ascii=False)

# format_assistant("renyajun")

def update_assistant(robot_name):
    robot_dir = os.path.join(workdir,'agents', robot_name)
    robot_json_path = os.path.join(robot_dir, 'robot.json')
    # 读取robot.json文件
    with open(robot_json_path, 'r') as f:
        robot = json.load(f)

    # 判断现在的assistant_info的md5值是否与robot.json文件中的assistant_md5值相同
    new_assistant_md5 = getmd5.json2md5(robot['assistant_info'])
    if robot['assistant_md5'] == new_assistant_md5:
        print("assistant_info没有更新")
        pass
    else:
        print("assistant_info更新了")
        robot['assistant_md5'] = new_assistant_md5
        baseapi.update_assistant(robot)

    # 判断现在的attact_file_info中的文件和原来的文件是不是一致，如果一直不做任何的修改，如果不一致就要更新。
    new_file_paths = []
    old_file_paths = robot['attact_file_info']['file_paths']

    for file_path in glob.glob(os.path.join(robot_dir, "*.txt")):
        new_file_paths.append(file_path)
    
    new_file_mad5s = []
    new_file_openai_ids = []

    added_files = list(set(new_file_paths) - set(old_file_paths))
    # print(f"新增文件：{added_files}")
    removed_files = list(set(old_file_paths) - set(new_file_paths))
    # print(f"删除的文件：{removed_files}")
    unchanged_files = list(set(old_file_paths).intersection(new_file_paths))
    # print(f"没有改动的文件：{unchanged_files}")
    
    for file_path in new_file_paths:
        if file_path in added_files:
            # 新增文件处理方式
            new_file_mad5s.append(getmd5.file2md5(file_path))
            new_file_openai_ids.append(baseapi.upload_file(file_path))
        if file_path in unchanged_files:
            # 没有改动的文件处理方式
            old_index = old_file_paths.index(file_path)
            # 判断此文件最新的md5 和之前的md5 是不是一致，一致的话取原来的 openai_id，不一致的话重新上传文件，还要删除原来的文件。
            if robot['attact_file_info']['file_md5s'][old_index] == getmd5.file2md5(file_path):
                new_file_mad5s.append(robot['attact_file_info']['file_md5s'][old_index])
                new_file_openai_ids.append(robot['attact_file_info']['file_openai_ids'][old_index])
            else:
                new_file_mad5s.append(getmd5.file2md5(file_path))
                new_file_openai_ids.append(baseapi.upload_file(file_path))
                # 删除原来的文件
                baseapi.delete_file(robot['attact_file_info']['file_openai_ids'][old_index])
                

    for file_path in removed_files:
        # 针对已经不存在的文件，删除对应的openai_file_id
        old_index = old_file_paths.index(file_path)
        baseapi.delete_file(robot['attact_file_info']['file_openai_ids'][old_index])

    robot['attact_file_info']['file_paths'] = new_file_paths
    robot['attact_file_info']['file_md5s'] = new_file_mad5s
    robot['attact_file_info']['file_openai_ids'] = new_file_openai_ids

    baseapi.attach_file_to_vector_store(robot)

    # 写入robot.json文件
    with open(robot_json_path, 'w' , encoding='utf-8') as f:
        json.dump(robot, f, indent=4,ensure_ascii=False)
    
# update_assistant("renyajun")