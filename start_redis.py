import os

def start_custom_redis():
    # 使用特定的配置文件启动Redis服务器
    # 这里我们假设配置文件为'my_redis.conf'，你可以根据需要进行调整
    os.system("redis-server /etc/redis/redis.conf &")  # & 使其在后台运行
    print("Custom Redis server with API keys started...")

if __name__ == "__main__":
    start_custom_redis()
