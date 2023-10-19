# Create Python file to extract the two main graphs created in the notebook
import pandas as pd
import matplotlib.pyplot as plt

def main():
    """Run the program as a whole."""
    
    # Colors to be used in graphs
    colors = ['#5E4FA2', '#75BBB4', '#BA6C65', '#6F88A1', '#A1A8D4', '#C5D9EA', '#EBCC77', '#E7A070', '#6A0572', '#AB83A1', '#E3E3E3']
    
    # Import the data and read it as pandas DataFrame
    space_df = pd.read_csv("Space_Corrected.csv")
    
    # Remove NaN entries
    space_df.dropna(inplace = True)
    
    # Removed Unnamed columns since they are useless
    space_df.drop([column for column in space_df.columns if "Unnamed" in column], axis = True, inplace = True)
    
    # Create "Years" Pandas column from "Datum" column using the "grab_year" function
    space_df["Year"] = space_df["Datum"].apply(grab_year)
    
    # Create "Country" Pandas column from "Location" column using the "grab_country" function
    space_df["Country"] = space_df["Location"].apply(grab_country)
    
    # Remove the "Datum" and "Location" columns since they contain too much detail and we do not need them anymore
    space_df.drop(["Datum", "Location"], axis = True, inplace = True)
    
    # Make a bar chart of countries against number of missions per country
    make_country_num_missions_graph(space_df, colors)
    
    # Make a bar chart of countries against percentage of successful missions per country
    make_country_success_percentage_graph(space_df, colors)

def grab_year(date):
    """Extract the year from the given date string."""
    
    _, year_containing = date.split(",")
    year = year_containing[1:5]
    return year

def grab_country(location):
    """Extract country from the given location string."""
    
    return location.split(",")[-1]

def grab_success_percentage(sub_data_frame):
    """Return a percentage that represents the successful missions of a country."""
    
    # Grab the total number of missions in that country
    num_country_missions = len(sub_data_frame)
    
    # Grab the total number of successful missions in that country
    num_country_successful_missions = len(sub_data_frame[sub_data_frame["Status Mission"] == "Success"])
    
    # Try to calculate the percentage and round it by two decimal places
    try:
        return round((num_country_successful_missions / num_country_missions) * 100, 2)
    
    except ZeroDivisionError:
        return round(0, 2)

def make_country_num_missions_graph(space_df, colors):
    """Make a Bar Chart about countries and the number of missions they had."""
    
    # Grab a list of all countries
    countries = space_df["Country"].unique()
    
    # Number of missions per country
    num_missions_per_country = []
    
    for country in countries:
        num_mission_per_country = len(space_df[space_df["Country"] == country])
        num_missions_per_country.append(num_mission_per_country)
    
    # Make a graph bar chart about countries vs success parcentage on space missions
    make_bar_chart(countries, num_missions_per_country,
                   "Number of Missions per Country",
                   "Country",
                   "Number of Missions",
                   colors,
                   "Countries",
                   "countries_n_mission_num_bar_chart.png")

def make_country_success_percentage_graph(space_df, colors):
    """Make a Bar Chart about countries and the percentage of success in their missions."""
    
    # Grab a list of all countries
    countries = space_df["Country"].unique()
    
    # Grab the success percentages per country
    countries_success_percentages = []
    
    # Loop through the countries
    for country in countries:
        
        # Calculate the success percentage of the current country
        country_success_percentage = grab_success_percentage(space_df[space_df["Country"] == country])
        
        # Append the current success percentage to the list of success percentages
        countries_success_percentages.append(country_success_percentage)
    
    # Make a graph bar chart about countries vs success percentage on space missions
    make_bar_chart(countries, countries_success_percentages,
                   "Success Percentage of Missions per Country",
                   "Country",
                   "Success Mission Percentage",
                   colors,
                   "Countries",
                   "countries_n_success_mission_percentage_bar_chart.png")

def make_bar_chart(x, y, title, xlabel, ylabel, colors, legend_title, filename):
    """Create a bar chart."""
    
    plt.figure(figsize = (20, 15))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.bar(x, y, color = colors, label = x)
    plt.legend(prop={"size": 15}, title = legend_title)
    plt.grid(axis = "y")
    plt.savefig(filename)
    plt.show()

if __name__ == "__main__":
    main()