import os
import redis

# 连接到Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
print(redis_client)

def set_api_keys():
    keys = ["123", "456","789"]  # 你的API密钥，此处部署在集群上后进行相应的修改
    redis_client.sadd("api_keys", *keys)
    print(f"Stored API keys: {keys}")
    
def save_keys_to_rdb():
    # 手动触发一个RDB保存
    redis_client.save()
    print("Keys saved to RDB.")

if __name__ == "__main__":
    set_api_keys()
    save_keys_to_rdb()