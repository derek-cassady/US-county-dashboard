import sys
import os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import subprocess
import requests

# Update the path to agesex.ipynb
filename = os.path.join(os.getcwd(), 'agesex.ipynb')
with open(filename) as aa:
    nb_in = nbformat.read(aa, nbformat.NO_CONVERT)

ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

nb_out = ep.preprocess(nb_in)

# Update the path to agesex_stats.ipynb
filename = os.path.join(os.getcwd(), 'agesex_stats.ipynb')
with open(filename) as aa:
    nb_in = nbformat.read(aa, nbformat.NO_CONVERT)

ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

nb_out = ep.preprocess(nb_in)

# '''Open and run the econ notebook'''
# filename = 'econ.ipynb'
# with open(filename) as bb:
#     nb_in = nbformat.read(bb, nbformat.NO_CONVERT)
    
# ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

# nb_out = ep.preprocess(nb_in)


# '''Open and run the income and benefits notebook'''
# filename = 'income_benefit.ipynb'
# with open(filename) as cc:
#     nb_in = nbformat.read(cc, nbformat.NO_CONVERT)
    
# ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

# nb_out = ep.preprocess(nb_in)

# Launch the Dash app
app_path = os.path.join(os.getcwd(), 'dash_app', 'app.py')
subprocess.Popen([sys.executable, app_path])

# Check if the Dash app is running
# Runs indefinitely until condition inside the loop is met
while True:
    try:
        # GET request to local server where the Dash app should be running
        response = requests.get("http://127.0.0.1:8050/")
        # '200', it means the app is up and running
        if response.status_code == 200:
            # executed, loop is broken
            break
        # Server is not yet running or is not reachable
    except requests.exceptions.ConnectionError:
        pass

# App is running, main.py can exit
sys.exit()