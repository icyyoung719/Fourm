import hashlib
import hmac

KEY = b'secret_key'  # 密钥

def encrypt(text):
    message = text.encode('utf-8')

    # 创建HMAC对象
    h = hmac.new(KEY, message, hashlib.sha1)
    # 获取HMAC的十六进制表示
    user_password_encrypted = h.hexdigest()

    return user_password_encrypted

def verify(text, encrypted_text):
    return encrypt(text) == encrypted_text