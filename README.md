# US-county-dashboard

## Project Background
This is the capstone project for Code Louisville Data Analysis 2.  The purpose 
of the project is to source demographic data for the population of the US and 
provide a general analysis to be explored through interactive dashboard.

In industry and practice, providiing easy to navigate visual data to end users 
is key to communication.  The more barriers placed in front of the end user
in accessing and operating analytics tools and reporting, the less effective the 
communication will be.

By stepping away from Excel, PowerBI, Tablaue and PowerPoint, we use a Python
Library called Dash which allows an interactive dashboard accessible by any web
browser.  This allows information to be consistently updated on the backend and
readily available to all users through a static source.  Allowing users ease of
access without having to search for the latest email and open files.

## Coder / Analyst Background
I have a Bachelors of Science in Occupational Health and Safety.  After working
for many years, as a First Responder I transferred my skills to industry.  I 
spent many years as a Safety Specialist for Amazon Fullfulment where I travelled
to many sites creating solution based training from opperational and safety data
and as a member of the internal audit teams.

While stepping away to raise a family, I have been keen to return to the 
workforce and expand on my knowledge in data analytics.  I hope to drive more
indepth understanding of safety concerns and leading indicators by pairing
operational, human resource, and safety data.  This would improve communications,
training, planning, and response for all aspects of  a business in regards to 
operating in safe, effecient, and qality manners.

## Code Background
The skills seen in the coding are after two 12 week courses through Code Louisville.
With very little experience in data analytics and only using Excel without VBA.

The coder chose to use ChatGPT 3.5 as a code assistant.  The purpose of choosing
this was to increase usage of methodology outside of the comfort zone of the 
coder.  Using ChatGPT 3.5 with its' known limitations and current state of being
out of date in many libraries and techniques would require accesing documentation and
problem solving beyond the learned skills.

## Project Requirements / Features
The project requirements come from a supplied table by Code Louisville.  The 
individual is allowed to choose at least one feature from each requirement 
section. The sections are listed below and the requirement location in the project
are noted further.

### Loading data:

#### Read TWO data files (JSON, CSV, Excel, etc.).
Data files are read in with agesex_stats.ipynb, and pg1.py.  The files are created 
in the project and saved as .xlsx files to be loaded as needed for further processing,
visualization, or communication.
#### Read TWO data sets in with an API
API are called in agesex_stats.ipynb, and further API calls were made in econ.ipynb
and income_benefit.ipynb which will be added to project later in the app.py
under pg2.py and pg3.py

### Clean and operate on the data while combining them:

#### Clean your data
Data cleaning is not needed for this project as the sources used provide clean
data through their APIs.  However, due to number of zeroes in the data, there
are many corrections made to deal with the zeros without causing 'NaN' issues.

Data combination, and further analysis of the data from the API pull is done
throughout agesex_stats.ipynb

### Visualize / Present your data:

#### Make 3 matplotlib or seaborn (or another plotting library)
The decision to use Dash as the final visualization meant more dependency on
Plotly.  Plotly has two plotting libraries, Plotly express, and Plotly Graph objects.
Plotly express is generally quicker to create, but has less overall customization.
Plotly Express was chosen as the grphing library for this project as UX/UI is 
not a primary consideration.

Plotly express allows you to create the base graph and it to Dash where you will
increase the interactivity of the graph in a web based dashboard.  This allows the
graph to be created in a simpler environment like a Jupyter notbook and then 
easily transferred into a web environment.

#### Make a Tableau dashboard to display your data
Dash was chosen as a web based solution for reasons stated prior in concerns
of user accessibility.  Dash was further considered as Plotly has libraries that
operate on other coding languages and skills learned in plotly will easily transfer
to other languages as skills expand or others review and use code.

#### Make a visualization with Bokeh. You can create interactive online visualizations
Dash was chosen over Bokeh for reasons stated previously, however, Bokeh was
considered.

### Best practices:

#### Utilize a virtual environment
A .venv was created and added to the .gitignore and used for all work on the
project.  Seperating the system environment, and any project environments is 
key to ensuring version control of libraries and python version deployments.

### Interpretation of your data:


#### Annotate your code with markdown cells in Jupyter Notebook,<br> 
#### write clear code comments,<br> 
#### and have a well-written README.md.

#### Annotate your .py files with well-written comments

### GitHub:

#### 5 commits is a minimum to show you’ve made multiple updates.


## How to Use

### Requirements

### API Keys

### Time

## Important Libraries

### Library decisions

## Future Update

### Known Bugs

