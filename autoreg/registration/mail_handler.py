"""
邮件处理器 - 使用 GPTMail 临时邮箱服务
https://mail.chatgpt.org.uk/
"""

from typing import Optional
from .gptmail_handler import GPTMailHandler, get_gptmail_handler


# 全局 handler 实例
_handler: Optional[GPTMailHandler] = None


def get_mail_handler(email_domain: str = None) -> Optional[GPTMailHandler]:
    """
    获取邮件处理器
    
    Args:
        email_domain: 忽略，GPTMail 自动分配域名
    
    Returns:
        GPTMailHandler 实例
    """
    global _handler
    
    if _handler is None:
        _handler = get_gptmail_handler()
    
    return _handler


def generate_email(prefix: Optional[str] = None) -> Optional[str]:
    """
    生成临时邮箱
    
    Args:
        prefix: 自定义前缀（可选）
    
    Returns:
        邮箱地址
    """
    handler = get_mail_handler()
    if handler:
        return handler.generate_email(prefix)
    return None


def get_verification_code(email: str, timeout: int = 300) -> Optional[str]:
    """
    获取验证码
    
    Args:
        email: 邮箱地址
        timeout: 超时时间（秒）
    
    Returns:
        验证码
    """
    handler = get_mail_handler()
    if handler:
        return handler.get_verification_code(email, timeout)
    return None


def clear_inbox(email: str) -> int:
    """
    清空邮箱
    
    Args:
        email: 邮箱地址
    
    Returns:
        删除的邮件数量
    """
    handler = get_mail_handler()
    if handler:
        return handler.clear_inbox(email)
    return 0
