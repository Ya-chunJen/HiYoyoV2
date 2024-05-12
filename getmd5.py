import json
import hashlib

# 计算字符串的 MD5 值
def str2md5(string_obj):
    md5_hash = hashlib.md5(string_obj.encode()).hexdigest()
    return md5_hash

# 计算JSONmd5值
def json2md5(json_obj):
    json_str = json.dumps(json_obj, sort_keys=True)
    md5_hash = hashlib.md5(json_str.encode()).hexdigest()
    return md5_hash

# 计算一个文件的md5值
def file2md5(file_path):
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()