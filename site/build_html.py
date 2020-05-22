import sys
import json

# (title,title,image,cook_time,servings,calories_per_serving,ingredients,directions,references,tags)
HTML_FORMAT = '''
<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
		<title>%s</title>
		<style type="text/css">body{margin:40px auto;max-width:650px;line-height:1.6;font-size:18px;color:#444;padding:0 10px}h1,h2,h3{line-height:1.2}</style>
	</head>
	<body>
		<h1>%s</h1>
		<img style="width:auto; height:350px;" src="%s">
		<p><em>Cook Time: %s</em></p>
		
		<h2>Seriving Information</h2>
		<ul>
			<li>Servings - %s</li>
			<li>Calories per Serving - %s</li>
		</ul>
		
		<h2>Ingredients</h2>
		<ul>
			%s
		</ul>
		
		<h2>Directions</h2>
		<p>%s</p>
		
		<h2>References</h2>
		<p>
			<ul>
				%s
			</ul>
		</p>

		<h2>Tags</h2>
		<p>
			%s
		</p>

		<br><hr>
		
		<p>
            <a href="/index.html">Home</a>&ensp;
			<a href="/recipes.html">Browse Recipes</a>&ensp;
			<a href="/tags.html">Browse Tags</a>&ensp;
            <a href="/edit.html">Edit Site</a>&ensp;
		</p>
	</body>
</html>
'''

def main():
    try:
        input_filename  = sys.argv[1]
        output_filename = sys.argv[2]
    except Exception:
        print("invalid argument(s)\nusage - build_html.py input.json output.html")
    #end try/except

    build_html_file(input_filename,output_filename)
#end main

def parse_file(filename):
    try:
        input_file = open(filename,"r")
    except Exception as e:
        print("Failed to open input file")
        print(e)
        return None
    #end try/except

    try:
        input_json = json.load(input_file)
        input_file.close()
    except Exception:
        print("Failed to parse input json")
        input_file.close()
        return None
    #end try/except

    return input_json
#end parse_file

def build_html(input_json):
    try:
        title     = input_json['title']
        
        image     = input_json['image']
        if(image == None): image = ''

        cook_time = input_json['cook_time']
        if(cook_time == None): cook_time = ''

        servings  = input_json['servings']
        if(servings == None): servings = ''

        calories_per_serving = input_json['calories_per_serving']
        if(calories_per_serving == None): calories_per_serving = ''

        ingredients = parse_ingredients_list(input_json['ingredients'])
        directions  = parse_directions(input_json['directions'])
        references  = parse_references(input_json['references'])
        tags        = parse_tags(input_json['tags'])
        
        recipe_html = HTML_FORMAT % (title,title,image,cook_time,servings,calories_per_serving,ingredients,directions,references,tags)
    except Exception as e:
        print("Failed to parse recipe data:")
        print(str(e))
        recipe_html = "invalid recipe data record"
    #end try/except

    return recipe_html
#end build_html()

def build_html_file(input_filename, output_filename):
    input_json = parse_file(input_filename)
    if(input_json == None): return

    try:
        output_file = open(output_filename,"w")
    except Exception as e:
        print("Failed to open output file")
        return
    #end try/except

    recipe_html = build_html(input_json)

    output_file.write(recipe_html)
    output_file.close()
#end build_html()

def parse_ingredients_list(ingredients_json):
    if(ingredients_json == None): return ''

    ingredients_html = ""
    for ingredient in ingredients_json:
        ingredients_html = ingredients_html + "<li>" + ingredient + "</li>"
    #endfor
    
    return ingredients_html
#end parse_ingredients_list()

def parse_directions(directions_json):
    if(directions_json == None): return ''

    return directions_json.replace("/p","</p><p>")
#end parse_directions()

def parse_references(references_json):
    if(references_json == None): return ''

    references_html = ""
    for reference in references_json:
        references_html = references_html + "<li><a href=\"" + reference['link'] + "\">"+ reference['name'] + "</a></li>"
    #endfor
    
    return references_html
#end parse_references()

def parse_tags(tags_json):
    if(tags_json == None): return ''

    tags_html = ""
    for tag in tags_json:
        tags_html = tags_html + "<a href=\"/tags/" + tag + ".html\">" + tag + "</a>&ensp;"
    #endfor
    return tags_html
#end parse_tags()

if __name__ == "__main__":
    main()