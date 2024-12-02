# Manage Local Project Virtual Environment

You should have a requirements.txt file that lists all packages the project needs.



## Open Project in VS Code for Terminal Commands

First, open your project in VS Code. 
Follow the instructions below to activate your local project virtual environment and install the necessary packages. 

## STEP A. CREATE A LOCAL PROJECT VIRTUAL ENV (.venv) USING PYTHON 3.10.11

Create your local project virtual environment
This step ensures you have an isolated Python environment for your project.
This is typically just done once at the beginning of a project.
If it gets messed up, we can delete .venv and recreate it at any time. 

## DELETE OLDER .venv

If (.venv) is active, use the deactivate command to release it. 

```
deactivate
```

Important: Delete any local project virtual environment in this project folder named .venv. 
Use Finder or any method to delete the whole folder permanently. 

## VERIFY LOCATION OF 3.10

On Windows, in VS Code, Open a new Terminal of the type PowerShell (not cmd).
Verify Python 3.10 is installed - USE YOUR PATH in the command below. 

```
C:\Users\edaci\AppData\Local\Programs\Python\Python310\python.exe --version
```

Verify you get 3.10.11

## CREATE NEW .venv WITH 3.10

Create a new .venv using Python 3.10 - USE YOUR PATH in the command below. 

```shell
C:\Users\edaci\AppData\Local\Programs\Python\Python310\python.exe -m venv .venv
```

## STEP B. ALWAYS ACTIVATE THE (.venv) WHEN WORKING ON YOUR PROJECT


ALWAYS activate the .venv before working on the project.
Activate whenever you open a new terminal. 

Windows PowerShell Command

```
.\.venv\Scripts\Activate.ps1
```

Mac/Linux Command

```
source .venv/bin/activate
```

Verify: When active, you can usually see (.venv) in the terminal.

If using a Jupyter notebook, select the kernel associated with your project (.venv).

## STEP C. INSTALL AND UPGRADE PACKAGES INTO (.venv) AS NEEDED

Install necessary packages listed below with this command.
Keep packages updated with the most recent versions.

When you identify a new package you want to use, 
Just update the list below and re-run this command. 

Windows Command

```
py -m pip install --upgrade -r requirements.txt
```

Mac/Linux Command

```
python3 -m pip install --upgrade -r requirements.txt
```

When you identify a new package you want to use, 
Just update the list below and re-run this command. 

