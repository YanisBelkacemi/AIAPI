import redis
from datetime import datetime
import hashlib
redisclient = redis.Redis(host="localhost" , port = 6379 , decode_responses=True)

def Token_daily(api_key):
    
    hashed_key = hashlib.sha224(api_key.encode()).hexdigest()

    # Today’s key
    today = datetime.utcnow().strftime("%Y-%m-%d")
    quota_key = f'qouta:{hashed_key}:day:{today}'

    # Get current usage
    current_usage = redisclient.get(quota_key)
    current_usage = int(current_usage) if current_usage else 0

    return current_usage