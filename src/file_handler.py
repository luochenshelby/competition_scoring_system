# 文件处理模块
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
    def save_results_excel(results_df: pd.DataFrame, filename: Optional[str] = None) -> str:
        """保存结果到Excel文件（可选功能）"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"比赛结果_{timestamp}.xlsx"

        filepath = RESULTS_DIR / filename

        try:
            # 创建Excel写入器
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                # 保存主结果
                results_df.to_excel(writer, sheet_name='比赛结果', index=False)

                # 添加统计信息工作表
                stats_data = {
                    '统计项': ['选手总数', '评委总数', '最高分', '最低分', '平均分'],
                    '数值': [
                        len(results_df),
                        results_df['评委人数'].iloc[0] if not results_df.empty else 0,
                        results_df['平均分'].max() if not results_df.empty else 0,
                        results_df['平均分'].min() if not results_df.empty else 0,
                        results_df['平均分'].mean() if not results_df.empty else 0
                    ]
                }
                stats_df = pd.DataFrame(stats_data)
                stats_df.to_excel(writer, sheet_name='统计信息', index=False)

            print(f"{Fore.GREEN}结果已保存到Excel文件: {filepath}{Style.RESET_ALL}")
            return str(filepath)
        except Exception as e:
            print(f"{Fore.RED}保存Excel文件时出错: {e}{Style.RESET_ALL}")
            return ""

    @staticmethod
    def save_results_json(results_df: pd.DataFrame, filename: Optional[str] = None) -> str:
        """保存结果到JSON文件"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"比赛结果_{timestamp}.json"

        filepath = RESULTS_DIR / filename

        try:
            # 转换为字典格式
            results_dict = results_df.to_dict(orient='records')

            # 添加元数据
            metadata = {
                "导出时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "数据量": len(results_dict),
                "文件格式": "JSON"
            }

            full_data = {
                "metadata": metadata,
                "results": results_dict
            }

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(full_data, f, indent=2, ensure_ascii=False)

            print(f"{Fore.GREEN}结果已保存到JSON文件: {filepath}{Style.RESET_ALL}")
            return str(filepath)
        except Exception as e:
            print(f"{Fore.RED}保存JSON文件时出错: {e}{Style.RESET_ALL}")
            return ""

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