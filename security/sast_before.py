import subprocess
def run_demo(user_value):
    return subprocess.run('echo '+user_value,shell=True,capture_output=True,text=True)
