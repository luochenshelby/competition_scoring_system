# config.py
import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).parent

# 数据文件路径
DATA_DIR = BASE_DIR / "data"
USERS_FILE = DATA_DIR / "users.json"
RESULTS_DIR = DATA_DIR / "results"

# 确保目录存在
DATA_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

# 系统配置
MAX_LOGIN_ATTEMPTS = 3
MIN_JUDGES = 3
MAX_JUDGES = 10
MIN_PLAYERS = 1
MAX_PLAYERS = 100
MIN_SCORE = 0
MAX_SCORE = 100