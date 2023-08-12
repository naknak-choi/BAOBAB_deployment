from django.core.mail import send_mail
import base64
import time

from django.conf import settings

def encode_data(data):
    return base64.urlsafe_b64encode(str(data).encode()).decode().rstrip('=')

def decode_data(encoded_data):
    padding = 4 - (len(encoded_data) % 4)
    encoded_data += '=' * padding
    return base64.urlsafe_b64decode(encoded_data.encode()).decode()

def generate_email_token(user):
    timestamp = time.time()
    encoded_id = encode_data(user.id)
    encoded_email = encode_data(user.email)
    encoded_timestamp = encode_data(timestamp)

    token = f"{encoded_id}.{encoded_email}.{encoded_timestamp}"
    return token

def verify_email_token(token):
    encoded_id, encoded_email, encoded_timestamp = token.split('.')
    print(encoded_id, encoded_email, encoded_timestamp)
    decoded_user_id = int(decode_data(encoded_id))
    decoded_email = decode_data(encoded_email)
    decoded_timestamp = float(decode_data(encoded_timestamp))

    return decoded_user_id, decoded_email, decoded_timestamp

def send_verification_email(user):
    token = generate_email_token(user)
    link = f"http://127.0.0.1:8000/user/verify_email/token={token}"

    subject = '[BAOBAB] 이메일 인증을 완료해주세요.'
    message = f'다음 링크를 클릭하여 이메일 인증을 완료해주세요: {link}'
    from_email = settings.EMAIL_HOST_USER # settings.py에서 설정한 발신 이메일
    recipient_list = [user.email]
    
    send_mail(subject, message, from_email, recipient_list)