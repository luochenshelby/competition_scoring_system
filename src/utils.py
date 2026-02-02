# 工具函数

import sys
from colorama import Fore, Style


def clear_screen():
    """清屏函数"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title):
    """打印标题"""
    print(f"\n{Fore.CYAN}{'=' * 60}")
    print(f"{' ' * (30 - len(title) // 2)}{title}")
    print(f"{'=' * 60}{Style.RESET_ALL}")


def print_menu(options):
    """打印菜单"""
    for key, description in options.items():
        print(f"  {Fore.GREEN}{key}.{Style.RESET_ALL} {description}")


def get_valid_input(prompt, input_type=str, valid_range=None, allow_empty=False):
    """获取有效输入"""
    while True:
        try:
            user_input = input(prompt).strip()

            if not user_input and not allow_empty:
                print(f"{Fore.RED}输入不能为空！{Style.RESET_ALL}")
                continue

            if input_type == int:
                value = int(user_input)
                if valid_range and (value < valid_range[0] or value > valid_range[1]):
                    print(f"{Fore.RED}输入必须在{valid_range[0]}到{valid_range[1]}之间！{Style.RESET_ALL}")
                    continue
                return value
            elif input_type == float:
                value = float(user_input)
                if valid_range and (value < valid_range[0] or value > valid_range[1]):
                    print(f"{Fore.RED}输入必须在{valid_range[0]}到{valid_range[1]}之间！{Style.RESET_ALL}")
                    continue
                return value
            else:
                return user_input
        except ValueError:
            print(f"{Fore.RED}请输入有效的{input_type.__name__}类型！{Style.RESET_ALL}")


def confirm_action(prompt="确定要执行此操作吗？"):
    """确认操作"""
    response = input(f"{prompt} ({Fore.GREEN}Y{Style.RESET_ALL}/{Fore.RED}N{Style.RESET_ALL}): ").strip().upper()
    return response == 'Y'