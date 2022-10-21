# TDI-Summer-2022-Capstone
*Ksenia Lisova*

My first own data science project where I analyzed crime reports in Los Angeles county and set up a simple navigation tool that finds the 'safest' walking path between two points based on historical crime locations. The web-app is deployed on Heroku for demonstration https://saferoute-tdi-2022.herokuapp.com/
(please forgive my noob HTML skills on that). Because crime reporting in the whole LA is not consistent I selected a small area of West Hollywood to make this proof-of-concept web app. The project can be easily expanded to any other geographical location where crime data is accessible.

I also included an in-depth visual analysis of crime dynamics in the **crime_viz.ipynb** file.


The data was obtained from lasd.org in a form of CSV files. After some dataset cleaning and merging I created pandas dataframes with all crimes in the years of 2018 - 2022 (incoplete latter year). I created a map using Folium library, and plotted the crime data using longitude and latitude parameters. I loaded street network information from OpenStreetMaps, processed each street with NetworkX library to add information about crimes in the street proximity as a weighting parameter. Using osmnx and NetworkX library I generated walking path between two points while minimizing encountered crimes.
