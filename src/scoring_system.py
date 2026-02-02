# 评分系统核心类
# scoring_system.py
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from dataclasses import dataclass
from datetime import datetime
from colorama import Fore, Style
from config import MIN_JUDGES, MAX_JUDGES, MIN_PLAYERS, MAX_PLAYERS


@dataclass
class Player:
    name: str
    scores: List[float]
    average_score: float = 0.0
    rank: int = 0


@dataclass
class Judge:
    name: str
    id: int


class ScoringSystem:
    def __init__(self):
        self.judges: List[Judge] = []
        self.players: List[Player] = []
        self.scoring_complete: bool = False

    def setup_judges(self) -> bool:
        """设置评委信息"""
        print(f"\n{Fore.CYAN}{'=' * 50}")
        print(f"{' ' * 10}设置评委信息")
        print(f"{'=' * 50}{Style.RESET_ALL}")

        try:
            num_judges = int(input(f"请输入评委人数 ({MIN_JUDGES}-{MAX_JUDGES}): "))

            if not (MIN_JUDGES <= num_judges <= MAX_JUDGES):
                print(f"{Fore.RED}评委人数必须在{MIN_JUDGES}到{MAX_JUDGES}之间！{Style.RESET_ALL}")
                return False
        except ValueError:
            print(f"{Fore.RED}请输入有效的数字！{Style.RESET_ALL}")
            return False

        self.judges.clear()
        for i in range(num_judges):
            while True:
                name = input(f"请输入第{i + 1}位评委姓名: ").strip()
                if name:
                    self.judges.append(Judge(name=name, id=i + 1))
                    break
                else:
                    print(f"{Fore.RED}评委姓名不能为空！{Style.RESET_ALL}")

        print(f"\n{Fore.GREEN}已成功设置 {len(self.judges)} 位评委:{Style.RESET_ALL}")
        for judge in self.judges:
            print(f"  评委{judge.id}: {judge.name}")

        return True

    def setup_players(self) -> bool:
        """设置选手信息"""
        print(f"\n{Fore.CYAN}{'=' * 50}")
        print(f"{' ' * 10}设置选手信息")
        print(f"{'=' * 50}{Style.RESET_ALL}")

        try:
            num_players = int(input(f"请输入选手人数 ({MIN_PLAYERS}-{MAX_PLAYERS}): "))

            if not (MIN_PLAYERS <= num_players <= MAX_PLAYERS):
                print(f"{Fore.RED}选手人数必须在{MIN_PLAYERS}到{MAX_PLAYERS}之间！{Style.RESET_ALL}")
                return False
        except ValueError:
            print(f"{Fore.RED}请输入有效的数字！{Style.RESET_ALL}")
            return False

        self.players.clear()
        for i in range(num_players):
            while True:
                name = input(f"请输入第{i + 1}位选手姓名: ").strip()
                if name:
                    self.players.append(Player(name=name, scores=[]))
                    break
                else:
                    print(f"{Fore.RED}选手姓名不能为空！{Style.RESET_ALL}")

        print(f"\n{Fore.GREEN}已成功设置 {len(self.players)} 位选手:{Style.RESET_ALL}")
        for i, player in enumerate(self.players, 1):
            print(f"  选手{i}: {player.name}")

        return True

    def collect_scores(self):
        """收集评委评分"""
        print(f"\n{Fore.CYAN}{'=' * 50}")
        print(f"{' ' * 10}开始评分")
        print(f"{'=' * 50}{Style.RESET_ALL}")

        if not self.judges:
            print(f"{Fore.RED}请先设置评委信息！{Style.RESET_ALL}")
            return False

        if not self.players:
            print(f"{Fore.RED}请先设置选手信息！{Style.RESET_ALL}")
            return False

        # 初始化所有选手的分数列表
        for player in self.players:
            player.scores = []

        # 为每位选手收集评委评分
        for i, player in enumerate(self.players, 1):
            print(f"\n{Fore.YELLOW}为选手 {player.name} 评分 ({i}/{len(self.players)}){Style.RESET_ALL}")

            for judge in self.judges:
                while True:
                    try:
                        score_input = input(f"  请 {judge.name} 评委为 {player.name} 打分 (0-100): ")
                        score = float(score_input)

                        if 0 <= score <= 100:
                            player.scores.append(score)
                            break
                        else:
                            print(f"{Fore.RED}  分数必须在0-100之间！{Style.RESET_ALL}")
                    except ValueError:
                        print(f"{Fore.RED}  请输入有效的数字！{Style.RESET_ALL}")

            print(f"  {Fore.BLUE}{player.name} 的评分: {player.scores}{Style.RESET_ALL}")

        self.scoring_complete = True
        return True

    def calculate_average_scores(self):
        """计算平均分（去掉最高分和最低分）"""
        if not self.scoring_complete:
            print(f"{Fore.RED}请先完成评分！{Style.RESET_ALL}")
            return

        for player in self.players:
            if len(player.scores) >= 3:
                # 去掉一个最高分和一个最低分
                sorted_scores = sorted(player.scores)
                trimmed_scores = sorted_scores[1:-1]
                player.average_score = round(np.mean(trimmed_scores), 2)
            elif len(player.scores) > 0:
                # 如果评委少于3人，直接计算平均分
                player.average_score = round(np.mean(player.scores), 2)
            else:
                player.average_score = 0.0

    def calculate_ranking(self):
        """计算排名"""
        self.calculate_average_scores()

        # 按平均分降序排序
        sorted_players = sorted(self.players, key=lambda x: x.average_score, reverse=True)

        # 计算名次（处理并列）
        current_rank = 1
        last_score = None
        same_score_count = 0

        for i, player in enumerate(sorted_players):
            if last_score is None:
                player.rank = current_rank
            elif player.average_score == last_score:
                # 并列情况
                same_score_count += 1
                player.rank = current_rank - same_score_count
            else:
                current_rank += 1 + same_score_count
                same_score_count = 0
                player.rank = current_rank

            last_score = player.average_score

        return sorted_players

    def display_results(self):
        """显示结果"""
        ranked_players = self.calculate_ranking()

        print(f"\n{Fore.CYAN}{'=' * 60}")
        print(f"{' ' * 15}比赛结果排名")
        print(f"{'=' * 60}{Style.RESET_ALL}")

        print(f"{'名次':<6} {'选手姓名':<15} {'平均分':<10} {'原始分数':<30}")
        print(f"{'-' * 60}")

        for player in ranked_players:
            scores_str = ", ".join([f"{s:.1f}" for s in player.scores])
            print(f"{player.rank:<6} {player.name:<15} "
                  f"{Fore.GREEN}{player.average_score:<10.2f}{Style.RESET_ALL} "
                  f"{scores_str:<30}")

        print(f"{'=' * 60}")

    def get_results_dataframe(self) -> pd.DataFrame:
        """将结果转换为DataFrame"""
        ranked_players = self.calculate_ranking()

        data = {
            '名次': [p.rank for p in ranked_players],
            '选手姓名': [p.name for p in ranked_players],
            '平均分': [p.average_score for p in ranked_players],
            '评委人数': [len(self.judges)] * len(ranked_players),
            '评分时间': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")] * len(ranked_players)
        }

        # 添加每位评委的评分
        for i, judge in enumerate(self.judges, 1):
            data[f'评委{i}评分'] = [p.scores[i - 1] if i - 1 < len(p.scores) else 0
                                    for p in ranked_players]

        return pd.DataFrame(data)