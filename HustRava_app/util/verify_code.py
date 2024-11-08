import string
import random

def generate_verify_code():
    """生成4位随机验证码"""
    return ''.join(random.choice(string.digits) for _ in range(4))