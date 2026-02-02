# 主程序入口
# main.py
import sys
import os
from colorama import Fore, Style, init

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.user_auth import UserAuth
from src.scoring_system import ScoringSystem
from src.file_handler import FileHandler
from src.utils import print_header, print_menu, get_valid_input, confirm_action

# 初始化colorama
init(autoreset=True)


class CompetitionApp:
    def __init__(self):
        self.auth = UserAuth()
        self.scoring_system = ScoringSystem()
        self.file_handler = FileHandler()
        self.running = True

    def main_menu(self):
        """主菜单"""
        while self.running:
            print_header("比赛评分系统主菜单")

            menu_options = {
                "1": "设置评委信息",
                "2": "设置选手信息",
                "3": "开始评分",
                "4": "查看当前排名",
                "5": "保存结果到文件",
                "6": "查看历史结果",
                "7": "用户管理",
                "8": "退出系统"
            }

            print_menu(menu_options)
            print(f"{'-' * 60}")

            choice = input(f"请选择操作 ({Fore.GREEN}1-8{Style.RESET_ALL}): ").strip()

            if choice == "1":
                self.setup_judges()
            elif choice == "2":
                self.setup_players()
            elif choice == "3":
                self.start_scoring()
            elif choice == "4":
                self.view_ranking()
            elif choice == "5":
                self.save_results()
            elif choice == "6":
                self.view_history()
            elif choice == "7":
                self.user_management()
            elif choice == "8":
                self.exit_system()
            else:
                print(f"{Fore.RED}无效选择，请重新输入！{Style.RESET_ALL}")

    def setup_judges(self):
        """设置评委"""
        if self.scoring_system.setup_judges():
            print(f"{Fore.GREEN}评委设置完成！{Style.RESET_ALL}")
        input(f"\n按{Fore.GREEN}Enter{Style.RESET_ALL}键继续...")

    def setup_players(self):
        """设置选手"""
        if self.scoring_system.setup_players():
            print(f"{Fore.GREEN}选手设置完成！{Style.RESET_ALL}")
        input(f"\n按{Fore.GREEN}Enter{Style.RESET_ALL}键继续...")

    def start_scoring(self):
        """开始评分"""
        if self.scoring_system.collect_scores():
            self.scoring_system.display_results()
        input(f"\n按{Fore.GREEN}Enter{Style.RESET_ALL}键继续...")

    def view_ranking(self):
        """查看排名"""
        if not self.scoring_system.scoring_complete:
            print(f"{Fore.RED}请先完成评分！{Style.RESET_ALL}")
        else:
            self.scoring_system.display_results()
        input(f"\n按{Fore.GREEN}Enter{Style.RESET_ALL}键继续...")

    def save_results(self):
        """保存结果到文件"""
        if not self.scoring_system.scoring_complete:
            print(f"{Fore.RED}请先完成评分！{Style.RESET_ALL}")
            input(f"\n按{Fore.GREEN}Enter{Style.RESET_ALL}键继续...")
            return

        results_df = self.scoring_system.get_results_dataframe()

        # 直接调用自动保存功能，默认保存为CSV
        self.file_handler.save_results_auto(results_df)

        input(f"\n按{Fore.GREEN}Enter{Style.RESET_ALL}键继续...")

    def view_history(self):
        """查看历史结果"""
        files = self.file_handler.list_saved_results()

        if files:
            choice = get_valid_input(
                f"\n选择要查看的文件编号 ({Fore.GREEN}0{Style.RESET_ALL}返回): ",
                input_type=int,
                valid_range=(0, len(files))
            )

            if choice > 0:
                selected_file = files[choice - 1]
                df = self.file_handler.load_results(selected_file)

                if df is not None and not df.empty:
                    print(f"\n{Fore.CYAN}{'=' * 60}")
                    print(f"文件内容: {selected_file.name}")
                    print(f"{'=' * 60}{Style.RESET_ALL}")
                    print(df.to_string(index=False))

        input(f"\n按{Fore.GREEN}Enter{Style.RESET_ALL}键继续...")

    def user_management(self):
        """用户管理（仅管理员）"""
        if self.auth.current_user != "admin":
            print(f"{Fore.RED}仅管理员可进行用户管理！{Style.RESET_ALL}")
            input(f"\n按{Fore.GREEN}Enter{Style.RESET_ALL}键继续...")
            return

        print_header("用户管理")

        user_options = {
            "1": "查看所有用户",
            "2": "添加新用户",
            "3": "返回主菜单"
        }

        print_menu(user_options)

        choice = input(f"请选择操作 ({Fore.GREEN}1-3{Style.RESET_ALL}): ").strip()

        if choice == "1":
            print(f"\n{Fore.CYAN}{'=' * 40}")
            print(f"{'用户名':<20} {'角色':<10}")
            print(f"{'=' * 40}{Style.RESET_ALL}")
            for username, info in self.auth.users.items():
                print(f"{username:<20} {info['role']:<10}")
            print(f"{'=' * 40}")

        elif choice == "2":
            new_username = input("输入新用户名: ").strip()
            if new_username in self.auth.users:
                print(f"{Fore.RED}用户名已存在！{Style.RESET_ALL}")
            else:
                new_password = input("输入密码: ").strip()
                role = get_valid_input("输入角色 (admin/judge/user): ").strip()

                if role not in ['admin', 'judge', 'user']:
                    role = 'user'

                if self.auth.add_user(new_username, new_password, role):
                    print(f"{Fore.GREEN}用户添加成功！{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}用户添加失败！{Style.RESET_ALL}")

        input(f"\n按{Fore.GREEN}Enter{Style.RESET_ALL}键继续...")

    def exit_system(self):
        """退出系统"""
        if confirm_action("确定要退出系统吗？"):
            self.running = False
            print(f"{Fore.BLUE}感谢使用比赛评分系统，再见！{Style.RESET_ALL}")

    def run(self):
        """运行应用程序"""
        print(f"{Fore.CYAN}{'=' * 60}")
        print(f"{' ' * 15}比赛简易评分系统")
        print(f"{' ' * 8}Anaconda + PyCharm 实现")
        print(f"{'=' * 60}{Style.RESET_ALL}")

        # 用户认证
        if self.auth.authenticate():
            self.main_menu()
        else:
            print(f"{Fore.RED}认证失败，程序退出{Style.RESET_ALL}")


def main():
    """主函数"""
    app = CompetitionApp()
    app.run()


if __name__ == "__main__":
    main()