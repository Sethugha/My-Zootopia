import requests
from dotenv import dotenv_values


def fetch_data(animal_name):
  """
  Fetches the animals data for the animal 'animal_name'.
  Returns: a list of animals, each animal is a dictionary:
  {
    'name': ...,
    'taxonomy': {
      ...
    },
    'locations': [
      ...
    ],
    'characteristics': {
      ...
    }
  },
  """
  config = dotenv_values(".env")
  api_url = 'https://api.api-ninjas.com/v1/animals?name={}'.format(animal_name)
  try:
      response = requests.get(api_url, headers=config)
      if response.status_code == requests.codes.ok:
          return response
      else:
          print("Error:", response.status_code, response.text)
  except Exception as e:
      print(f"Error: Something went wrong with the request. Exception {e}")
