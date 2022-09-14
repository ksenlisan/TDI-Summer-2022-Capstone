# TDI-Summer-2022-Capstone
*Ksenia Lisova*

Deployed on Heroku https://saferoute-tdi-2022.herokuapp.com/

# SafeRoute (West Hollywood): A navigation algorithm for improved safety
SafeRoute algorithms prioritizes street safety instead of distance to come up with a route which historically had the least amount of crime occurrences. The proof of concept SafeRoute project is set in West Hollywood area of Los Angeles, but can be expanded to any other geographical location where crime data is accessible.

West Hollywood in Los Angeles attracts many people, tourists and locals alike for its numerous bars and music venues, historical landmarks and celebrity hangouts.  Located next to Beverly Hills area it’s placement and pop culture significance makes it one of the must visit places in Los Angeles. Despite its popularity, crime is soaring in West Hollywood and many people are concerned about public safety. As a Los Angeles resident I don’t always feel safe when I am outside especially in a less familiar area. Because criminal awareness is not advertised to the public, it is often hard to say whether  the area you are in is safer or more dangerous. With SafeRoute project I am addressing the needs of tourists and locals who wish to prioritize their safety when picking a walking route between their points of interest. 

While crime occurrences in West Hollywood are generally high – the density of the occurrences is not uniform. Using Los Angeles Sheriff’s department website we can access the information about crime occurrences with their geographical location. I created a map using Folium library, and plotted the crime data using longitude and latitude parameters. I loaded street network information from OpenStreetMaps, processed each street with NetworkX library to add information about crimes in the street proximity. Using osmnx library I setup an algorithm that would generate a walking path between two points while minimizing encountered crimes.

The SafeRoute West Hollywood will be available as a web page where a user can enter desired points of origin and destination to display available shortest and safest navigation routes for walking.
