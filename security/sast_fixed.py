import subprocess
def run_demo(user_value):
    return subprocess.run(['echo',user_value],shell=False,capture_output=True,text=True,check=True)
