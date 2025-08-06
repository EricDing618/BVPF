import mmap

class FuckWifi:
    def __init__(self):
        
def process_text_with_mmap(file_path, process_func):
    with open(file_path, "rb") as f:  # 必须用二进制模式
        # 创建内存映射（只读模式）
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            # 逐行读取（返回的是 bytes，需解码）
            for line in iter(mm.readline, b""):
                decoded_line = line.decode("utf-8").strip()  # 解码 + 去除换行
                process_func(decoded_line)  # 处理每行