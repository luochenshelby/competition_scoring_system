# file_handler.py
import pandas as pd
import json
import csv
from pathlib import Path
from datetime import datetime
from typing import Optional
from config import RESULTS_DIR
from colorama import Fore, Style


class FileHandler:
    @staticmethod
    def save_results_csv(results_df: pd.DataFrame, filename: Optional[str] = None) -> str:
        """保存结果到CSV文件"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"比赛结果_{timestamp}.csv"

        filepath = RESULTS_DIR / filename

        try:
            results_df.to_csv(filepath, index=False, encoding='utf-8-sig')
            print(f"{Fore.GREEN}结果已保存到CSV文件: {filepath}{Style.RESET_ALL}")
            return str(filepath)
        except Exception as e:
            print(f"{Fore.RED}保存CSV文件时出错: {e}{Style.RESET_ALL}")
            return ""

    @staticmethod
    def save_results_auto(results_df: pd.DataFrame, filename: Optional[str] = None) -> str:
        """自动保存结果为CSV文件（主入口函数）"""
        print(f"\n{Fore.CYAN}{'=' * 50}")
        print(f"{' ' * 15}保存结果到文件")
        print(f"{'=' * 50}{Style.RESET_ALL}")

        # 询问用户是否使用自定义文件名
        custom_name = input(f"输入文件名（留空使用默认名称）: ").strip()

        if custom_name:
            # 确保文件名有.csv扩展名
            if not custom_name.endswith('.csv'):
                custom_name += '.csv'
            filename = custom_name
        else:
            # 使用默认文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"比赛结果_{timestamp}.csv"

        # 保存为CSV
        return FileHandler.save_results_csv(results_df, filename)

    @staticmethod
    def list_saved_results():
        """列出已保存的结果文件"""
        files = list(RESULTS_DIR.glob("*"))

        if not files:
            print(f"{Fore.YELLOW}暂无已保存的结果文件{Style.RESET_ALL}")
            return []

        print(f"\n{Fore.CYAN}{'=' * 60}")
        print(f"{' ' * 15}已保存的结果文件")
        print(f"{'=' * 60}{Style.RESET_ALL}")

        for i, file in enumerate(sorted(files, key=lambda x: x.stat().st_mtime, reverse=True), 1):
            size_kb = file.stat().st_size / 1024
            mtime = datetime.fromtimestamp(file.stat().st_mtime)
            print(f"{i:2d}. {file.name:<40} {size_kb:.1f}KB  {mtime.strftime('%Y-%m-%d %H:%M')}")

        return files

    @staticmethod
    def load_results(filepath: Path) -> Optional[pd.DataFrame]:
        """加载结果文件"""
        try:
            if filepath.suffix.lower() == '.csv':
                return pd.read_csv(filepath, encoding='utf-8-sig')
            elif filepath.suffix.lower() == '.xlsx':
                return pd.read_excel(filepath, sheet_name='比赛结果')
            elif filepath.suffix.lower() == '.json':
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return pd.DataFrame(data['results'])
            else:
                print(f"{Fore.RED}不支持的文件格式: {filepath.suffix}{Style.RESET_ALL}")
                return None
        except Exception as e:
            print(f"{Fore.RED}加载文件时出错: {e}{Style.RESET_ALL}")
            return None