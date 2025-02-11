import os
from pathlib import Path

project_name="src"

list_of_files=[

    f"{project_name}/__init__.py",
    f"{project_name}/helper.py",
    f"{project_name}/prompt.py",
    f"research/trials.ipynb",
    '.env',
    "setup.py",
    "app.py",
    




]
for path in list_of_files:
    filepath=Path(path)

    filedir,filename=os.path.split(path)
    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
   
