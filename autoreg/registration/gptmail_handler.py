"""
GPTMail 临时邮箱 API Handler
使用 https://mail.chatgpt.org.uk/ 的 API 获取验证码
"""

import re
import time
import requests
from typing import Optional

import sys
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass


class GPTMailHandler:
    """GPTMail 临时邮箱处理器"""
    
    BASE_URL = 'https://mail.chatgpt.org.uk/api'
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
        })
    
    def generate_email(self, prefix: Optional[str] = None) -> Optional[str]:
        """
        生成邮箱地址
        
        Args:
            prefix: 自定义前缀（可选），1-32字符，只允许 [a-zA-Z0-9._-]
        
        Returns:
            生成的邮箱地址或 None
        """
        try:
            if prefix:
                resp = self.session.post(
                    f'{self.BASE_URL}/custom-email',
                    json={'prefix': prefix}
                )
            else:
                resp = self.session.get(f'{self.BASE_URL}/generate-email')
            
            if resp.status_code == 200:
                data = resp.json()
                email = data.get('email')
                if email:
                    print(f'[OK] Generated email: {email}')
                    return email
            
            print(f'[FAIL] Generate email failed: {resp.text}')
            return None
            
        except Exception as e:
            print(f'[FAIL] Generate email error: {e}')
            return None
    
    def get_emails(self, email: str) -> list:
        """获取邮箱中的所有邮件"""
        try:
            resp = self.session.get(
                f'{self.BASE_URL}/get-emails',
                params={'email': email}
            )
            if resp.status_code == 200:
                return resp.json().get('emails', [])
            return []
        except Exception as e:
            print(f'[WARN] Get emails error: {e}')
            return []
    
    def get_verification_code(self, email: str, timeout: int = 300) -> Optional[str]:
        """
        等待并获取 AWS 验证码
        
        Args:
            email: 邮箱地址
            timeout: 超时时间（秒）
        
        Returns:
            6位验证码或 None
        """
        import random
        
        start_time = time.time()
        checked_ids = set()
        poll_count = 0
        
        print(f'[MAIL] Waiting for verification code to {email}...')
        
        while time.time() - start_time < timeout:
            try:
                emails = self.get_emails(email)
                
                for mail in emails:
                    mail_id = mail.get('id')
                    if mail_id in checked_ids:
                        continue
                    
                    checked_ids.add(mail_id)
                    
                    # 检查是否来自 AWS
                    sender = mail.get('from', '').lower()
                    subject = mail.get('subject', '').lower()
                    
                    if 'aws' not in sender and 'amazon' not in sender:
                        continue
                    
                    if 'verify' not in subject and 'code' not in subject:
                        continue
                    
                    print(f'   [FOUND] Email from AWS: {mail.get("subject", "")[:50]}')
                    
                    code = self._extract_code(mail)
                    if code:
                        print(f'[OK] Found verification code: {code}')
                        return code
                
                poll_count += 1
                wait_time = random.uniform(3.0, 6.0)
                
                if poll_count % 5 == 0:
                    elapsed = int(time.time() - start_time)
                    print(f'   [WAIT] Polling... ({elapsed}s)')
                
                time.sleep(wait_time)
                
            except Exception as e:
                print(f'[WARN] Poll error: {e}')
                time.sleep(5)
        
        print(f'[FAIL] Verification code not found in {timeout}s')
        return None
    
    def _extract_code(self, mail: dict) -> Optional[str]:
        """从邮件中提取6位验证码"""
        body = mail.get('textContent', '')
        
        if not body:
            html = mail.get('htmlContent', '')
            body = re.sub(r'<[^>]+>', ' ', html)
            body = re.sub(r'\s+', ' ', body)
        
        patterns = [
            r'verification code[:\s]+(\d{6})',
            r'Your code[:\s]+(\d{6})',
            r'code is[:\s]+(\d{6})',
            r'code[:\s]+(\d{6})',
            r'>(\d{6})<',
            r'\b(\d{6})\b',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, body, re.IGNORECASE)
            if match:
                code = match.group(1)
                if len(code) == 6 and code.isdigit():
                    return code
        
        return None
    
    def clear_inbox(self, email: str) -> bool:
        """清空邮箱"""
        try:
            resp = self.session.post(
                f'{self.BASE_URL}/clear-inbox',
                json={'email': email}
            )
            return resp.status_code == 200
        except:
            return False
    
    def disconnect(self):
        """关闭连接"""
        self.session.close()


def get_gptmail_handler() -> GPTMailHandler:
    """获取 GPTMail handler 实例"""
    return GPTMailHandler()
