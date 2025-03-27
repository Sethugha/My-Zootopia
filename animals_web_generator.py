import json


def load_data(file_path):
    """loads a json file"""
    with open(file_path, "r") as handle:
        return json.load(handle)

def insert_into_html(file_path, text):
    """loads a html file"""
    with open(file_path, "r") as infile:
        htmlcode = infile.read()

    with open(file_path, "w") as outfile:
        outfile.write(htmlcode.replace("__REPLACE_ANIMALS_INFO__", text))


def main():
    animals_data = load_data("animals_data.json")

    output = ""
    for animal in animals_data:
        if 'name' in animal:
            output += f"\nName: {animal['name']}\n"
        if 'diet' in animal['characteristics']:
            output += f"Diet: {animal['characteristics']['diet']}\n"
        if 'locations' in animal and animal['locations']:
            output += f"Location: {animal['locations'][0]}\n"
        if 'type' in animal['characteristics']:
            output += f"Type: {animal['characteristics']['type']}\n"
    insert_into_html("animals_template.html", output.replace("\n","<br>"))


if __name__ == "__main__":
    main()
