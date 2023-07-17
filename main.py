import subprocess

# Run agesex.ipynb notebook using subprocess
agesex_process = subprocess.Popen(['jupyter', 'nbconvert', '--execute', 'agesex.ipynb'])

# Wait for agesex_process to complete
agesex_process.wait()