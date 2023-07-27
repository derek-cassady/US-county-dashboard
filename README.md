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
training, planning, and response for all aspects of a business in regards to 
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

#### Read TWO data files.
Data files are read in with agesex_stats.ipynb, and pg1.py.  The files are created 
in the project and saved as .xlsx files to be loaded as needed for further processing,
visualization, or communication.

#### Read TWO data sets with an API
APIs are called in agesex_stats.ipynb, and further API calls were made in econ.ipynb
and income_benefit.ipynb which will be added to project later in the app.py
under pg2.py and pg3.py

### Clean and operate:

#### Clean your data
Data cleaning is not needed for this project as the sources used provide clean
data through their APIs.  However, due to number of zeroes in the data, there
are many corrections made to deal with the zeros without causing 'NaN' issues.

Data combination, and further analysis of the data from the API pull is done
throughout agesex_stats.ipynb

### Visualize / Present your data:

#### Make 3 visuals
The decision to use Dash as the final visualization meant more dependency on
Plotly.  Plotly has two plotting libraries, Plotly express, and Plotly Graph objects.
Plotly express is generally quicker to create, but has less overall customization.
Plotly Express was chosen as the grphing library for this project as UX/UI is 
not a primary consideration.

Plotly express allows you to create the base graph and add it to Dash where you will
increase the interactivity of the graph in a web based dashboard.  This allows the
graph to be created in a simpler environment like a Jupyter notbook and then 
easily transferred into a python file for further development.

#### Make a dashboard
Dash was chosen as a web based solution for reasons stated prior in concerns
of user accessibility.  Dash was further considered as Plotly has libraries that
operate on other coding languages and skills learned in plotly will easily transfer
to other languages as skills expand or others review and use code.

### Best practices:

#### Utilize a virtual environment
A .venv was created, added to the .gitignore and used for all work on the
project.  Seperating the system environment, and any project environments is 
key to ensuring version control of libraries and python version deployments.

### Interpretation of your data:

#### Annotate your code
Commenting of code is a skill that is in need of constant improvement.  Jupyter
files are commented using a mix of markdown and in cell comments.  Commenting
code during reviews and edit of code is ongoing for further clarity.

### GitHub:

#### 5 commits is a minimum
Github updates are frequently made while making changes to code and moving from
file to file.  Some updates are missed and best practices and good habits are
still being built.

## How to Use

### Requirements
This project was done in a Windows environment and uses pathing that works in 
a windows environment.  Therefore, in its' current state, it can not be guarenteed
to work in a Mac or Linux based system.

Please ensure that if you are using a virtual environment it is contained within the project cloned file:
```\US-county-dashboard\.venv```

In your environment, please install the requirements found in requirements.txt by doing the following:

```pip install -r requirements.txt```

Please verify afterwards that the following were installed with the noted versions by performing a ```pip freeze```.  If not, you will need to update them accordingly:

nbclient==0.8.0<br>
nbconvert==7.7.3<br>
nbformat==5.9.1<br>
ipykernel==6.25.0<br>
ipython==8.14.0<br>

If you would like to attempt running in a Mac or Linux based system, at minimum, you
will need to remove 'pywin32==306' from requirements.txt and replace with the Mac or
Linux equivelent as pywin32 provides some Windows specific package managing and
bindings.

### API Keys
API keys have been removed from the files agesex.ipynb, econ.ipynb, and 
income_benefit.ipynb

To run the entirity of the project you will need to retrieve keys from the
U.S. Census Bureau and Bureau of Economic Analysis.  Links to sign up for a key
are provided below.  Once you have a key, past it into the location provided in
the Jupyter Notebooks.

For files: agesex.ipynb & income_benefit.ipynb<br>
https://api.census.gov/data/key_signup.html<br>

For file: econ.ipynb<br>
https://apps.bea.gov/api/signup/<br>

### Time
Due to the number of API calls, exports to excel, and excel loading, the project
can take 30 - 60 minutes to produce the dashboard.  Please be patient.  Once the
dashboard has loaded, you will see a link in your terminal to the dashboard hosted
on your system.

Once this is complete, the dashboard is responsive with minimal lag. When finished, CTRL + C in the terminal to end.

Some systems may encounter errors while excel files are being created, or read in.
These are system intensive steps and errors can occur during read or write cycles, if
you would like clean copies of the excel files to run the app only, please let me know.


## Important Libraries
[requests](https://requests.readthedocs.io/en/latest/)<br>
```pip install requests```<br>
[dash](https://dash.plotly.com/)<br>
```pip install dash```<br>
[pandas](https://pandas.pydata.org/)<br>
```pip install pandas```<br>
[plotly express](https://plotly.com/python-api-reference/plotly.express.html)<br>
```pip install plotly-express```<br>
[nbconvert](https://nbconvert.readthedocs.io/en/latest/)<br>
```pip install nbconvert```<br>
[openpyxl](https://openpyxl.readthedocs.io/en/stable/)<br>
```pip install openpyxl```

## Future Update
Further visualizations for the dataframes exported to 'Statistics_Dataframes'
will be added.  These will allow for further drill down into the age and sex makeup
of each individual race in the counties of the US.

Further data analysis work needs to be completed on the information pulled in
for econ.ipynb, and income_benefit.ipynb.  Once completed, the visualizations will
be added to pg2.py and pg3.py which will run as part of the dashboard and be intermixed
with hoverdata in each visualization where needed.

### Known Bugs
On running requirements.txt some users are not having the proper versions of ipykernel and ipython installed.  This is a possible issue with version of PIP, but has not been verified.

There are 4 -5 missing points of data for Alaska and one county in Colorado. This
is a bug in the way the JSON file is being read for those specific FIPS codes.
Further troubleshooting is needed to provide a workaround for the JSON load in.

The Alaska choropleth map is noted as being an issue with Dash.  Currently there
no known work around for including it in the functionality of the main map for all states.
The Dash community has noted this issue in the community forums and in the plotly
feature requests.

