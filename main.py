import subprocess
import IPython

# Open the agesex.ipynb notebook
print("Opening the notebook...")
IPython.Application.instance().kernel.do_shutdown(restart=False)

# Run agesex.ipynb notebook using subprocess
print("Running the notebook...")
agesex_process = subprocess.run(["jupyter", "nbconvert", "--execute", "agesex.ipynb"])

# Check if there was an error while running the notebook
if agesex_process.returncode != 0:
    print("Error: Failed to run the notebook.")
else:
    print("Notebook execution completed successfully.")

# Close the notebook
print("Closing the notebook...")
IPython.Application.instance().kernel.do_shutdown(restart=False)