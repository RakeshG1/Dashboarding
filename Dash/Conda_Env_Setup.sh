#!/bin/sh

# Conda Version
conda -V 

# List Existing Conda Environments in System
conda info --envs

# Update Conda
conda update conda

# Upgrade PIP
pip install --upgrade pip

# Remove Existing Old Env
conda env remove -n DASH_ENV

# Create Conda Environment
conda create --name DASH_ENV python=3.10.4 -y

# Activate Conda Environment
conda activate DASH_ENV

# Install Python Packages
# Check python library version here : https://pypi.org/project/jupyter-dash/
pip install -r Requirements.txt

# Check Python Libraries
conda list 
pip freeze

# To just generate html report from jupyter notebook
jupyter nbconvert --to html xxxx.ipynb

# To execute & generate html report from jupyter notebook
jupyter-nbconvert --execute --ExecutePreprocessor.timeout=900 s--to html xxxx.ipynb

# Execute Dash Dashboards Creation Script
(DASH_ENV) XXX $ python Dash_Demo.py 

# Stop Execution : Shortcut Key
ctrl + z

# For python-kernel to run syntax in jupyter/ipython notebook
python -m ipykernel install --user

# To enable conda commands in shell env
$(conda shell.bash hook)

# Conda Env Export 
conda env export > DASH_ENV.yml

# Python Version
python --version
# Python 3.10.4

# Python Path
which python
# /opt/anaconda3/envs/DASH_ENV/bin/python

# Deactivate Conda Environment
conda deactivate