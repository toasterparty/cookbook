import os
import json
from flask import Flask
from flask import render_template
from build_html import build_html
from build_html import parse_file

app = Flask(__name__)

# static routes #

@app.route('/')
def root():
    return render_template("index.html")

@app.route('/<page>')
def static_route(page):
    return render_template(page)

# static routes - dynamic pages #

RECIPES_FORMAT = '''
<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
		<title>All Recipes</title>
		<style type="text/css">body{margin:40px auto;max-width:650px;line-height:1.6;font-size:18px;color:#444;padding:0 10px}h1,h2,h3{line-height:1.2}</style>
        <style>
        table {
            font-family: arial, sans-serif;
            border-collapse: collapse;
            width: 100%%;
        }

        td, th {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }

        tr:nth-child(even) {
            background-color: #dddddd;
        }
        </style>
	</head>
	<body>
		<h1>All Recipes</h1>
        <p>
            <table>
                <tr>
                    <th>Name</th>
                    <th>Calories Per Serving</th>
                    <th>Cook Time</th>
                </tr>
                %s
            </table>
        </p>
	</body>
</html>
'''

RECIPES_TABLE_ROW_FORMAT = '''
<tr>
    <th><a href="%s">%s</a></th>
    <th>%s</th>
    <th>%s</th>
</tr>
'''

@app.route('/recipes.html')
def recipes():
    table_html = ''

    directory = os.fsencode("./recipes")
    for file in os.listdir(directory):
        try:
            filename = os.fsdecode(file)
            if filename.endswith(".json"): 
                recipe_json = parse_file('./recipes/' + filename)
                table_html = table_html + (RECIPES_TABLE_ROW_FORMAT % ('/recipes/' + filename.replace('.json','.html'),recipe_json['title'],recipe_json['calories_per_serving'],recipe_json['cook_time']))
            #endif
        except Exception as e:
            print(filename + ' error:')
            print('\t' + str(e))
    #endfor

    return RECIPES_FORMAT % (table_html)
# end recipes()

@app.route('/tags.html')
def tags():
    return 'not implemented'
# end recipes()

# dynamic routes - dynamic pages #

@app.route('/recipes/<page>')
def recipe(page):
    input_json = parse_file('./recipes/' + page.replace('.html','.json'))
    if(input_json == None): return "recipe not found or corrupted"

    return build_html(input_json)
#end recipe()

@app.route('/tags/<page>')
def tag(page):
    return 'not implemented'
#end recipe()

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', threaded=True)