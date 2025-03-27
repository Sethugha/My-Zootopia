import json


def load_data(file_path):
    """loads a json file"""
    with open(file_path, "r") as handle:
        return json.load(handle)


def insert_into_html(file_path, text):
    """inserts text into a html file
    :parameter file_path: Pat to the html-template
    :parameter text: Text to replace the wildcard with.
    :return: None
    """
    with open(file_path, "r") as infile:
        htmlcode = infile.read()
    with open(file_path, "w") as outfile:
        outfile.write(htmlcode.replace("__REPLACE_ANIMALS_INFO__", text))


def serialize_animal(animal_obj):
    output = ''
    output += "<li class='cards__item'>"
    output += f"<div class='card__title'>{animal_obj['name']}</div>"
    output += f"<p class='card__text'>"
    if 'diet' in animal_obj['characteristics']:
        output += f"<strong>Diet:</strong> {animal_obj['characteristics']['diet']}<br/>"
    if 'locations' in animal_obj and animal_obj['locations']:
        output += f"<strong>Location:</strong> {animal_obj['locations'][0]}<br/>"
    if 'type' in animal_obj['characteristics']:
        output += f"<strong>Type:</strong> {animal_obj['characteristics']['type']}<br/>"
    output += "</p></li>"
    return output


def main():
    animals_data = load_data("animals_data.json")
    output = ""
    for animal_obj in animals_data:
        output += serialize_animal(animal_obj)
    insert_into_html("animals_template.html", output)


if __name__ == "__main__":
    main()
