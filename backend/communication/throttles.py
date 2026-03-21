from .services.redis_client import redisclient
from datetime import datetime
from rest_framework.throttling import BaseThrottle
from rest_framework.exceptions import Throttled
import hashlib

class QuotaLimitting():
    Dlimit = 100
    def allow_request(self , request , view):
        #checking the APikey
        apikey = request.headers.get('Api-Key')
        if not apikey:
            return False
        #hashing it
        hash_key = hashlib.sha224(apikey.encode()).hexdigest()
        #thsi section here is used to create a redis quota
        today = datetime.utcnow().strftime("%Y-%m-%d")
        quota_key = f'qouta:{hash_key}:day:{today}'
        #adding 1 for each req
        current = redisclient.incr(quota_key)
        #expiring after 2days
        if current ==1 :
            redisclient.expire(quota_key , 60*60*24*2)
        #costum error handling when the limit is exceeded
        if current > self.Dlimit:
            raise Throttled(
                detail=f"Daily quota exceeded. You made {current} requests; limit is {self.Dlimit}.",
                code="quota_exceeded"
            )
        return current <= self.Dlimit
    
    def wait(self):
        return None