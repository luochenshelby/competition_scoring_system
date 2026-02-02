# 用户认证模块
# user_auth.py
import json
import hashlib
from pathlib import Path
from config import USERS_FILE
from colorama import Fore, Style, init

# 初始化colorama
init(autoreset=True)


class UserAuth:
    def __init__(self):
        self.users = self.load_users()
        self.current_user = None
        self.login_attempts = 0

    @staticmethod
    def hash_password(password):
        """使用SHA256加密密码"""
        return hashlib.sha256(password.encode()).hexdigest()

    def load_users(self):
        """从文件加载用户数据"""
        if USERS_FILE.exists():
            try:
                with open(USERS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self.create_default_users()
        else:
            return self.create_default_users()

    def create_default_users(self):
        """创建默认用户"""
        default_users = {
            "admin": {
                "password": self.hash_password("admin123"),
                "role": "admin"
            },
            "judge": {
                "password": self.hash_password("judge123"),
                "role": "judge"
            },
            "user": {
                "password": self.hash_password("user123"),
                "role": "user"
            }
        }

        # 保存到文件
        self.save_users(default_users)
        return default_users

    def save_users(self, users_data=None):
        """保存用户数据到文件"""
        if users_data is None:
            users_data = self.users

        try:
            with open(USERS_FILE, 'w', encoding='utf-8') as f:
                json.dump(users_data, f, indent=2, ensure_ascii=False)
            return True
        except IOError:
            return False

    def authenticate(self):
        """用户认证"""
        print(f"\n{Fore.CYAN}{'=' * 50}")
        print(f"{' ' * 10}比赛评分系统登录")
        print(f"{'=' * 50}{Style.RESET_ALL}")

        while self.login_attempts < 3:
            print(f"\n{Fore.YELLOW}尝试 {self.login_attempts + 1}/3{Style.RESET_ALL}")
            username = input(f"{Fore.GREEN}用户名: {Style.RESET_ALL}").strip()
            password = input(f"{Fore.GREEN}密码: {Style.RESET_ALL}").strip()

            if self.validate_credentials(username, password):
                self.current_user = username
                role = self.users[username]["role"]
                print(f"\n{Fore.GREEN}登录成功！欢迎{role}: {username}{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.RED}用户名或密码错误！{Style.RESET_ALL}")
                self.login_attempts += 1

        print(f"\n{Fore.RED}错误次数超过限制，系统退出！{Style.RESET_ALL}")
        return False

    def validate_credentials(self, username, password):
        """验证用户凭据"""
        if username in self.users:
            hashed_password = self.hash_password(password)
            return self.users[username]["password"] == hashed_password
        return False

    def add_user(self, username, password, role="user"):
        """添加新用户"""
        if username not in self.users:
            self.users[username] = {
                "password": self.hash_password(password),
                "role": role
            }
            self.save_users()
            return True
        return False

    def logout(self):
        """注销当前用户"""
        self.current_user = None
        self.login_attempts = 0
        print(f"{Fore.BLUE}已安全退出登录{Style.RESET_ALL}")