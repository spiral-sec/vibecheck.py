#!/bin/python3.9

# For simplicity reasons, this script will only run with Python3.
# If Python3 is not installed, you can use this script:
# https://github.com/cervoise/linuxprivcheck/blob/master/linuxprivchecker3.py

from colorama import Fore, Style
import subprocess as s
import sys

class Command:
    def __init__(self, command: str, comment: str, alternative: str = ''):
        self.command = command
        self.comment = comment
        self.alternative = alternative
        self.output = ''

    def run_command_wrapper(self) -> str:
        out, _ = s.Popen(
                [self.command], stdout=s.PIPE, stderr=s.PIPE, shell=True
                ).communicate()
        if out == '' and self.alternative != '':
            out, _ = s.Popen(
                    [self.alternative], stdout=s.PIPE, stderr=s.PIPE, shell=True
                    ).communicate()
        return out.decode('utf-8').strip()

    def run(self):
        self.output = self.run_command_wrapper()
        if self.output == '':
            print(f'{Fore.RED} [-] Not output for {self.comment}{Style.RESET_ALL}')
        else:
            print(f'{Fore.GREEN} [+] {self.comment}:\n{Style.RESET_ALL}{self.output}')


#################################
######### ENUMERATION ###########
#################################

print(f'{Fore.YELLOW}[*] System Info{Style.RESET_ALL}')
Command("hostnamectl | grep 'Operating System | cut -d : -f 2'", "Operating System").run()
Command("cat /proc/version", "Kernel version").run()
Command("hostname", "Hostname").run()

print(f'\n{Fore.YELLOW}[*] Network Info{Style.RESET_ALL}')
Command("/sbin/ifconfig -a", "Network Interfaces", "ip address show").run()
Command("route", "Route", "ip route").run()
Command("netstat -antup | grep -v 'TIME_WAIT'",
        "Network status", "ss -lut | grep -v 'TIME_WAIT'").run()

print(f'\n{Fore.YELLOW}[*] Filesystem Info{Style.RESET_ALL}')
Command("mount", "mount output").run()
Command("cat /etc/fstab 2>/dev/null", "fstab entries").run()

print(f'\n{Fore.YELLOW}[*] Cron jobs{Style.RESET_ALL}')
Command("ls -la /etc/cron* 2>/dev/null", "Scheduled cron jobs").run()
Command("ls -laR /etc/cron 2>/dev/null | awk '$1 ~ /w.$/' 2>/dev/null",
        "Writable cron jobs").run()

print(f'\n{Fore.YELLOW}[*] Current user info{Style.RESET_ALL}')
Command("whoami", "Current user").run()
Command("id", "Current user id").run()
Command("cat /etc/passwd", "All users").run()
Command("grep -v -E '^#' /etc/passwd | awk -F: '$3 == 0{print $1}'",
        "Super users").run()
Command("grep 'docker\|lxd' /etc/group", "Users in Docker group").run()
Command("env 2>/dev/null | grep -v 'LS_COLORS'", "Env values").run()
Command("cat /etc/sudoers 2>dev/null | grep -v '#' 2>/dev/null",
        "sudoers file").run()
Command("w 2>/dev/null", "user's activity").run()
Command("ls /tmp/ssh* 2>dev/null",
        "SSH Agent connection (lookup ssh agent hijacking)").run()
Command("screen -ls 2>/dev/null", "Screen active socket").run()
Command("tmux ls 2>/dev/null", "Tmux active socket").run()

