import data_fetcher as df


TRANSLATION_TABLE = str.maketrans({8217: "&rsquo;", 180: "&lsquo;", 196: "&Auml;",
                                    228: "&auml;", 214: "&Ouml;", 246: "&ouml;",
                                    220: "&Uuml;", 252: "&uuml;"
                                   })

def load_html_template(filepath):
    with open(filepath, "r") as infile:
        html_template_code = infile.read()
    return html_template_code


def save_html_file(filepath, file_contents):
    with open(filepath, "w") as outfile:
        outfile.write(file_contents)


def insert_animal_data_into_html(text):
    """inserts text into a html file
    :parameter text: Text to replace the wildcard with.
    :return: None
    """
    html_template_code = load_html_template("animals_template.html")
    text = text.translate(TRANSLATION_TABLE)
    animals_page_contents = html_template_code.replace("__REPLACE_ANIMALS_INFO__", text)
    save_html_file("animals.html", animals_page_contents)


def create_unknown_species_error_content(failed_species):
    output = ''
    output += "<li class='cards__item'>"
    output += f"<div class='card__title'>{failed_species}</div>"
    output += "<div class='card__text'><ul>"
    output += f"<li><strong>Sorry:</strong> Unknown Species {failed_species}</li>"
    output += "</ul></div></li>"
    return output


def serialize_animal(animal_obj):
    """Converts the JSON data from a single animal_object
    into an eye-friendly html-card
    :parameter animal_object: single object from datasource
    """
    card = "<li class='cards__item'><div class='card__title'>"
    animal_name = animal_obj.get('name', 'Unnamed Subspecies')
    card += animal_name+"</div>"
    card += "<div class='card__text'><ul>"
    if animal_obj.get('locations', 'N/A') != 'N/A':
        locations = animal_obj.get('locations')
        card += "<h3><strong>Locations: </strong></h3>"
        for location in locations:
            card += f"<li>{location}</li>"
    if animal_obj.get('characteristics', 'N/A') != 'N/A':
        card += "<h3>Characteristics:</h3>"
        for key, val in animal_obj['characteristics'].items():
            val = animal_obj['characteristics'].get(key, 'N/A')
            card += f"<li><strong>{key.replace('_',' ').capitalize()}:</strong> {val}</li>"
    if animal_obj.get('taxonomy', 'N/A') != 'N/A':
        card += "<h3>Taxonomy:</h3>"
        for key, val in animal_obj['taxonomy'].items():
            val = animal_obj['taxonomy'].get(key, 'N/A')
            card += f"<li><strong>{key.replace('_',' ').capitalize()}:</strong> {val}</li>"
        card += "</ul></div></li>"
    return card


def main():
    animal_html_content = ""
    animal = input("Enter a name of an animal: ")
    response = df.fetch_data(animal)
    if response.json():
        for animal_obj in response.json():
            animal_html_content += serialize_animal(animal_obj)
        insert_animal_data_into_html(animal_html_content)
        print("Website was successfully generated to the file animals.html")
    else:
        animal_html_content = create_unknown_species_error_content(animal)
        insert_animal_data_into_html(animal_html_content)
        print("Website was successfully generated to the file animals.html")


if __name__ == "__main__":
    main()
