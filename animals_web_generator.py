import requests
from dotenv import dotenv_values


TRANSLATION_TABLE = str.maketrans({8217: "&rsquo;", 180: "&lsquo;", 196: "&Auml;",
                                    228: "&auml;", 214: "&Ouml;", 246: "&ouml;",
                                    220: "&Uuml;", 252: "&uuml;"
                                   })


def send_get_request(name):
    """Sends a single get request to animals-api. Returns complete response
    The necessary API-key is imported via dotenv.
    :parameter name: Complete or part of an animal identifier
    """
    config = dotenv_values(".env_orig")
    api_url = 'https://api.api-ninjas.com/v1/animals?name={}'.format(name)
    try:
        response = requests.get(api_url, headers=config)
        if response.status_code == requests.codes.ok:
            return response
        else:
            print("Error:", response.status_code, response.text)
    except Exception as e:
        print(f"Error: Something went wrong with the request. Exception {e}")


def insert_into_html(text):
    """inserts text into a html file. The insertion is also used to replace
    some special characters with their html-code.
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
    animal_html_content = ""
    animal = input("Enter a name of an animal: ")
    try:
        response = send_get_request(animal)
        if response.json():
            for animal in response.json():
                animal_html_content += serialize_animal(animal)
            insert_into_html(animal_html_content)
            print("Website was successfully generated to the file animals.html")
        else:
            print("Sorry: Unknown Species: No data available")
    except AttributeError:
        print("Sorry, something went wrong with the API-response")


if __name__ == "__main__":
    main()
