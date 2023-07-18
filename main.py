import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import subprocess
import requests

'''Open and run the agesex notebook'''
filename = 'agesex.ipynb'
with open(filename) as aa:
    nb_in = nbformat.read(aa, nbformat.NO_CONVERT)
    
ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

nb_out = ep.preprocess(nb_in)

'''Open and run the econ notebook'''
filename = 'econ.ipynb'
with open(filename) as bb:
    nb_in = nbformat.read(bb, nbformat.NO_CONVERT)
    
ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

nb_out = ep.preprocess(nb_in)


'''Open and run the income and benefits notebook'''
filename = 'income_benefit.ipynb'
with open(filename) as cc:
    nb_in = nbformat.read(cc, nbformat.NO_CONVERT)
    
ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

nb_out = ep.preprocess(nb_in)

# Launch the Dash app
subprocess.Popen(["python", "dash.py"])

# Check if the Dash app is running
while True:
    try:
        response = requests.get("http://127.0.0.1:8050/")
        if response.status_code == 200:
            break
    except requests.exceptions.ConnectionError:
        pass

# The Dash app is now running, so the main.py script can exit