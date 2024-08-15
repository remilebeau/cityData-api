import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# load .env file
load_dotenv()

# cors
origins = []
if os.getenv("PYTHON_ENV") == "development":
    origins = ["http://localhost:3000"]
else:
    origins = [
        "https://remilebeau-citydata.vercel.app",
    ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @desc fetch city data
# @route GET /api/citydata
# @access public
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
            "DC": "District of Columbia",
            "D.C.": "District of Columbia",
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
    # format state
    state = state.title().replace(" ", "-")
    # special formatting for Washington, DC
    if state == "District-Of-Columbia":
        state = "District-of-Columbia"

    # send request
    url = f"https://www.city-data.com/city/{city}-{state}.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # get name
    name = soup.find("h1").text

    # check value of name to validate response
    if name == "Oops, Page Not Found!":
        raise HTTPException(status_code=404, detail="City not found")

    # get population and populationChange
    population = soup.find("section", class_="city-population").text.split(". ")[0]
    populationChange = soup.find("section", class_="city-population").text.split(". ")[
        1
    ]

    # get medianIncome and medianHomeValue
    medianIncome = soup.find("section", class_="median-income").text.split("\n")[0]
    medianHomeValue = soup.find("section", class_="median-income").text.split("\n")[4]

    # get and validate crimeRate
    crimeRate = soup.find("section", class_="crime")
    if not crimeRate:
        crimeRate = ""
    else:
        crimeRate = crimeRate.find("tr", class_="nosort").find_all("td")[-1].text

    # get education and commute
    education_and_commute_elements = soup.find(
        "section", class_="education-info"
    ).find_all("li")
    education_and_commute = []
    for li in education_and_commute_elements:
        education_and_commute.append(li.text)

    # get nearestCities
    nearestCities = soup.find("section", class_="nearest-cities").text.replace(
        " )", ")"
    )

    # return data
    return {
        "name": name,
        "population": population,
        "populationChange": populationChange,
        "medianIncome": medianIncome,
        "medianHomeValue": medianHomeValue,
        "crimeRate": crimeRate,
        "educationAndCommute": education_and_commute,
        "nearestCities": nearestCities,
    }
