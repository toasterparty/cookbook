import sys
import json

HEADER
FOOTER

def main():
    try:
        input_filename  = sys.argv[1]
        output_filename = sys.argv[2]
    except Exception:
        print("invalid argument(s)\nusage - build_html.py input.json output.html")
    #end try/except

    build_html(input_filename,output_filename)
#end main

def build_html(input_filename, output_filename):
    try:
        input_file = open(input_filename,"r")
    except Exception:
        print("Failed to open input file")
        return
    #end try/except

    try:
        input_json = json.load(input_file)
    except Exception:
        print("Failed to parse input json")
        input_file.close()
        return
    #end try/except

    try:
        output_file = open(output_filename,"w")
    except Exception as e:
        print("Failed to open output file")
        return
    #end try/except

    try:
        title     = input_json['title']
        cook_time = input_json['cook_time']
        servings  = input_json['servings']
        calories_per_serving = input_json['calories_per_serving']
        ingredients = parse_ingredients_list(input_json['ingredients'])
        directions = parse_directions(input_json['directions'])
        references = parse_references(input_json['references'])
        tags = parse_tags(input_json['tags'])

        print("Successfully built " + output_filename)
    except Exception:
        print("Failed to parse recipe data")
    #end try/except

    input_file.close()
    output_file.close()
#end build_html()

def parse_ingredients_list(ingredients_json):
    return str(ingredients_json)
#end parse_ingredients_list()

def parse_directions(directions_json):
    return str(directions_json)
#end parse_directions()

def parse_references(references_json):
    return str(references_json)
#end parse_references()

def parse_tags(tags_json):
    return str(tags_json)
#end parse_tags()

if __name__ == "__main__":
    main()