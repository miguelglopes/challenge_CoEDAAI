import json
from data import config  # local


class Country:

    def __init__(self, country_name: str, population: int, continent: str):
        """Creates a country

        Arguments:
            country_name {str} -- Country name
            population {int} -- Country population
            continent {str} -- Country continent
        """
        self.country_name = country_name
        self.population = population
        self.continent = continent

    def get_population_in_millions(self) -> float:
        """Returns the country population in millions, with 2 decimal digits

        Returns:
            float -- Country population in millions, with 2 decimal digits
        """
        return round(float(self.population)/1000000, 2)


def import_data() -> dict:
    """ Read Json data from a file into a dictionary. The json file path is config.jsonPath.

    Returns:
        dict -- dictionary with the data contained in the config.jsonPath file. Countries dictionary
    """
    with open(config.jsonPath) as f:
        return json.load(f)


# ??? should it change the original dictionary? It's not clear from the question. That's what I did
# ??? looking at the population values, it is clear that the original dictionary already had the area in sq km, not sq miles
def convert_population_to_int(countries: dict) -> dict:
    """Converts each country population into int type

    Arguments:
        countries {dict} -- Countries dictionary

    Returns:
        dict -- Updated countries dictionary
    """
    for k, v in countries.items():
        v["Population"] = int(v["Population"])
    return countries

# ??? should it change the original dictionary? It's not clear from the question. That's what I did.


def convert_area_to_sq_km(countries: dict) -> dict:
    """Converts each country area into sq km

    Arguments:
        countries {dict} -- Countries dictionary

    Returns:
        dict -- Updated countries dictionary
    """
    for k, v in countries.items():
        v["Area"] = round(float(v["Area"])*2.58999, 1)
    return countries


def get_europe_countries(countries: dict) -> list:
    """Gets list of all european countries names present in the countries dictionary

    Arguments:
        countries {dict} -- Countries dictionary

    Returns:
        list -- List of european countries names
    """
    countriesL = [c for c in countries if countries[c]["Continent"] == "Europe"]
    countriesL.sort()
    return countriesL


def get_literacy_levels_by_continent(countries: dict, continent: str) -> list:
    """Computes the literacy level as:
        - literacy in [0, 25[ % - VERY_LOW
        - literacy in [25, 50[ % - LOW
        - literacy in [50, 70[ % - MEDIUM
        - literacy in [70, 90[ % - HIGH
        - literacy in [90, 100] % - VERY_HIGH

    Arguments:
        countries {dict} -- Countries dictionary
        continent {str} -- Continent. If continent is not in the countries dictionary, an empty lsit will be returned.

    Raises:
        Exception: raises exception if input literacy level is unknown (higher than 100 or lower than 0)

    Returns:
        list -- list of tuples like [(country_1, literacy_1, literacy_level_1), ..., (country_n, literacy_n,literacy_level_n), ...]
    """

    # RFE this could be done with a dictionary in the config file
    def getLiteracyLevel(literacy):
        if 0 <= v["Literacy"] < 25:
            return "VERY_LOW"
        elif 25 <= v["Literacy"] < 50:
            return "LOW"
        elif 50 <= v["Literacy"] < 70:
            return "MEDIUM"
        elif 70 <= v["Literacy"] < 90:
            return "HIGH"
        elif 90 <= v["Literacy"] <= 100:
            return "VERY_HIGH"
        else:
            raise Exception("Unkown literacy level")

    # ??? if continent doesnt exist, it will return an empy list. Is it the desired behavior?
    literacyL = []
    for k, v in countries.items():
        if v["Continent"] == continent:
            literacyL.append((k, v["Literacy"], getLiteracyLevel(v["Literacy"])))

    return literacyL


def get_country_codes(countries: dict) -> list:
    """ Gets country codes from the countries dictionary. Sstrips all characters that are not letters from the country name,
        gets the first 3 characters (or as many as there are until 3) and converts them to uppercase.

    Arguments:
        countries {dict} -- [description]

    Returns:
        list -- [description]
    """
    return list(map(lambda c: ''.join(filter(str.isalpha, c))[:3].upper(), countries.keys()))


def get_country_population(countries: dict, country_name: str) -> float:
    """ Gets the country population in millions, with 2 decimal digits

    Arguments:
        countries {dict} -- Countries dictionary
        country_name {str} -- Country name

    Returns:
        float -- country population in million or None, if the country doesn't exist.
    """

    try:
        country = Country(country_name, countries[country_name]["Population"], countries[country_name]["Continent"])
        return country.get_population_in_millions()
    except KeyError:
        print("There is no information for the country " + country_name)
        return
