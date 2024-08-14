import requests
from bs4 import BeautifulSoup

from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/api/citydata")
def fetch_city_data(city: str, state: str):
    # format city
    city = city.title().replace(" ", "-")
    # format state
    # convert state code to full state name
    if len(state) == 2:
        state = state.upper()
        states = {
            "AL": "Alabama",
            "AK": "Alaska",
            "AZ": "Arizona",
            "AR": "Arkansas",
            "CA": "California",
            "CO": "Colorado",
            "CT": "Connecticut",
            "DE": "Delaware",
            "FL": "Florida",
            "GA": "Georgia",
            "HI": "Hawaii",
            "ID": "Idaho",
            "IL": "Illinois",
            "IN": "Indiana",
            "IA": "Iowa",
            "KS": "Kansas",
            "KY": "Kentucky",
            "LA": "Louisiana",
            "ME": "Maine",
            "MD": "Maryland",
            "MA": "Massachusetts",
            "MI": "Michigan",
            "MN": "Minnesota",
            "MS": "Mississippi",
            "MO": "Missouri",
            "MT": "Montana",
            "NE": "Nebraska",
            "NV": "Nevada",
            "NH": "New Hampshire",
            "NJ": "New Jersey",
            "NM": "New Mexico",
            "NY": "New York",
            "NC": "North Carolina",
            "ND": "North Dakota",
            "OH": "Ohio",
            "OK": "Oklahoma",
            "OR": "Oregon",
            "PA": "Pennsylvania",
            "RI": "Rhode Island",
            "SC": "South Carolina",
            "SD": "South Dakota",
            "TN": "Tennessee",
            "TX": "Texas",
            "UT": "Utah",
            "VT": "Vermont",
            "VA": "Virginia",
            "WA": "Washington",
            "WV": "West Virginia",
            "WI": "Wisconsin",
            "WY": "Wyoming",
        }
        state = states.get(state)
    state = state.title().replace(" ", "-")
    url = f"https://www.city-data.com/city/{city}-{state}.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    name = soup.find("h1").text
    if name == "Oops, Page Not Found!":
        raise HTTPException(status_code=404, detail="City not found")
    population = soup.find("section", class_="city-population").text.split(". ")[0]
    populationChange = soup.find("section", class_="city-population").text.split(". ")[
        1
    ]
    medianIncome = soup.find("section", class_="median-income").text.split("\n")[0]
    medianHomeValue = soup.find("section", class_="median-income").text.split("\n")[4]
    nearestCities = soup.find("section", class_="nearest-cities").text
    return {
        "name": name,
        "population": population,
        "populationChange": populationChange,
        "medianIncome": medianIncome,
        "medianHomeValue": medianHomeValue,
        "nearestCities": nearestCities,
    }
