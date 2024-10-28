# smart-store-mhoyt

## Table of Contents
- [Project Setup](#project-setup)
- [Commit to GitHub](#commit-to-github)

## Project Setup
Run all commands from a terminal in the root project folder.

### Step 1 - Create a Local Project Virtual Environment
```bash
py -m venv .venv
```

### Step 2 - Activate the Virtual Environment
```bash
.venv\Scripts\activate
```

### Step 3 - Install Packages
```bash
py -m pip install --upgrade -r requirements.txt
```

### Step 4 - Optional: Verify .venv Setup
```bash
py -m datafun_venv_checker.venv_checker
```

### Step 5 - Run the Initial Project Script
```bash
py scripts\data_prep.py
```

## Commit to GitHub

### Step 1 – Add All New Files to Source Control
```bash
git add .
```

### Step 2 - Commit with a Message Describing Changes
```bash
git commit -m "add starter files"
```

### Step 3 - Push the Changes to the Origin on Branch `main`
```bash
git push -u origin main
```
