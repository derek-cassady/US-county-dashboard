import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

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