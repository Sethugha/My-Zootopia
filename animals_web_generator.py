"""
import requests

name = 'cheetah'
api_url = 'https://api.api-ninjas.com/v1/animals?name={}'.format(name)
response = requests.get(api_url, headers={'X-Api-Key': 'AazlY6Wbh9RvPfdYMSJq3A==0eHAHVdy9q1rTzWQ'})
if response.status_code == requests.codes.ok:
    print(response.text)
else:
    print("Error:", response.status_code, response.text)

"""


import requests
from dotenv import dotenv_values

TRANSLATION_TABLE = str.maketrans({8217: "&rsquo;", 180: "&lsquo;", 196: "&Auml;",
                                    228: "&auml;", 214: "&Ouml;", 246: "&ouml;",
                                    220: "&Uuml;", 252: "&uuml;"
                                   })


def send_get_request(name):
    """Sends a single get request to animals-api. Returns complete response"""
    config = dotenv_values(".env")
    api_url = 'https://api.api-ninjas.com/v1/animals?name={}'.format(name)
    response = requests.get(api_url, headers=config)
    print(response.status_code)
    try:
        if response.status_code == requests.codes.ok:
            return response
        else:
            print("Error:", response.status_code, response.text)
    except Exception as e:
        print(f"Error: Something went wrong with the request. Exception {e}")


def insert_into_html(text):
    """inserts text into a html file
    :parameter file_path: Pat to the html-template
    :parameter text: Text to replace the wildcard with.
    :return: None
    """
    template = "animals_template.html"
    text = text.translate(TRANSLATION_TABLE)
    with open(template, "r") as infile:
        htmlcode = infile.read()
    with open("animals.html", "w") as outfile:
        outfile.write(htmlcode.replace("__REPLACE_ANIMALS_INFO__", text))


def serialize_animal(animal_obj, selection = ""):
    """extracts desired values from a single animal_object
    :parameter animal_object: single object from datasource
    :parameter selection: if given, returns only values for objects with characteristic
    """
    if not animal_obj.get('characteristics'):
        return ""
    if animal_obj['characteristics'].get('skin_type'):
        if selection and selection.lower() not in animal_obj['characteristics']['skin_type'].lower():
            return ""
        output = ''
        output += "<li class='cards__item'>"
        output += f"<div class='card__title'>{animal_obj['name']}</div>"
        output += f"<div class='card__text'><ul>"
        if animal_obj['characteristics'].get('diet'):
            output += f"<li><strong>Diet:</strong> {animal_obj['characteristics']['diet']}</li>"
        if animal_obj.get('locations'):
            output += f"<li><strong>Location:</strong> {animal_obj['locations'][0]}</li>"
        if animal_obj['characteristics'].get('type'):
            output += f"<li><strong>Type:</strong> {animal_obj['characteristics']['type']}</li>"
        output += "</ul></div></li>"
    return output


def main():
    html_addon = ""
    animal = input("Enter a name of an animal: ")
    try:
        response = send_get_request(animal)
        if response.json():
            for animal in response.json():
                html_addon += serialize_animal(animal)
            insert_into_html(html_addon)
            print("Website was successfully generated to the file animals.html")
        else:
            print("Sorry: Unknown Species: No data available")
    except AttributeError:
        print("Sorry, something went wrong with json-contents")




if __name__ == "__main__":
    main()
