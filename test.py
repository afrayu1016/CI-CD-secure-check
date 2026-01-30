import subprocess

def run_user_code(user_input):
    # HIGH: code injection
    eval(user_input) # nosec

def run_command(cmd):
    # HIGH: command injection
    subprocess.Popen(cmd, shell=True)

def ignored_case(data):
    exec(data)  # nosec
