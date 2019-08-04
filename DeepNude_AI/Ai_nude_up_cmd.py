import os
import sys,os,subprocess

com=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))+r"\python3.7\python.exe "+ os.path.dirname(__file__)+"/Ai_nude_up.py"
p2 = subprocess.Popen(com,shell=True,stdout=subprocess.PIPE)
p2.wait()

