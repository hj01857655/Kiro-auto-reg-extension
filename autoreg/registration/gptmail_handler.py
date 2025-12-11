"""
GPTMail 临时邮箱 API Handler
使用 https://mail.chatgpt.org.uk/ 的 API 获取验证码
无需配置，自动生成临时邮箱
"""

import re
import time
import requests
import urllib3
from typing import Optional

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import sys
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass


class GPTMailHandler:
    """GPTMail 临时邮箱处理器"""
    
    BASE_URL = 'https://mail.chatgpt.org.uk'
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'accept': 'application/json',
            'content-type': 'application/json',
            'referer': 'https://mail.chatgpt.org.uk/',
            'origin': 'https://mail.chatgpt.org.uk'
        })
        self.session.verify = False
        self.current_email = None
    
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
                    f'{self.BASE_URL}/api/generate-email',
                    json={'prefix': prefix}
                )
            else:
                resp = self.session.get(f'{self.BASE_URL}/api/generate-email')
            
            if resp.status_code == 200:
                data = resp.json()
                if data.get('success'):
                    email = data.get('data', {}).get('email')
                    if email:
                        self.current_email = email
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
                f'{self.BASE_URL}/api/emails',
                params={'email': email}
            )
            if resp.status_code == 200:
                data = resp.json()
                if data.get('success'):
                    return data.get('data', {}).get('emails', [])
            return []
        except Exception as e:
            print(f'[WARN] Get emails error: {e}')
            return []
    
    def connect(self) -> bool:
        """连接测试（生成一个邮箱验证 API 可用）"""
        email = self.generate_email()
        return email is not None
    
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
                    sender = mail.get('from_address', '').lower()
                    subject = mail.get('subject', '').lower()
                    
                    if 'aws' not in sender and 'amazon' not in sender:
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
        # 优先用纯文本
        body = mail.get('content', '')
        
        # 如果没有，用 HTML
        if not body:
            html = mail.get('html_content', '')
            body = re.sub(r'<[^>]+>', ' ', html)
            body = re.sub(r'\s+', ' ', body)
        
        # 验证码匹配模式
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
    
    def delete_email(self, email_id: str) -> bool:
        """
        删除单封邮件
        
        Args:
            email_id: 邮件 ID
        
        Returns:
            是否删除成功
        """
        try:
            resp = self.session.delete(f'{self.BASE_URL}/api/email/{email_id}')
            if resp.status_code == 200:
                data = resp.json()
                if data.get('success'):
                    print(f'[OK] Deleted email: {email_id}')
                    return True
            print(f'[FAIL] Delete email failed: {resp.text}')
            return False
        except Exception as e:
            print(f'[FAIL] Delete email error: {e}')
            return False
    
    def clear_inbox(self, email: str) -> int:
        """
        清空邮箱
        
        Args:
            email: 邮箱地址
        
        Returns:
            删除的邮件数量
        """
        try:
            resp = self.session.delete(
                f'{self.BASE_URL}/api/emails/clear',
                params={'email': email}
            )
            if resp.status_code == 200:
                data = resp.json()
                if data.get('success'):
                    count = data.get('data', {}).get('count', 0)
                    print(f'[OK] Cleared inbox: {count} emails deleted')
                    return count
            print(f'[FAIL] Clear inbox failed: {resp.text}')
            return 0
        except Exception as e:
            print(f'[FAIL] Clear inbox error: {e}')
            return 0
    
    def disconnect(self):
        """关闭连接"""
        self.session.close()


def get_gptmail_handler() -> GPTMailHandler:
    """获取 GPTMail handler 实例"""
    handler = GPTMailHandler()
    return handler
