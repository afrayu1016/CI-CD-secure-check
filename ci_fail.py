import os
import subprocess
import pickle
import yaml
import hashlib
import requests

password = "123456"

def dangerous():
    eval("print('hello')")
    exec("print('world')")

    os.system("ls -la")
    subprocess.call("ls -la", shell=True)
    subprocess.run("ls -la", shell=True)

    data = pickle.loads(b"cos\nsystem\n(S'ls'\ntR.")
    yaml.load("!!python/object/apply:os.system ['ls']")

    m = hashlib.md5(b"password").hexdigest()

    requests.get("https://example.com", verify=False)

dangerous()
