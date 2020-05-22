import os
import sys
import json
from flask import Flask, render_template, request
from build_html import build_html, parse_file

app = Flask(__name__)

# static routes #

@app.route('/')
def root():
    return render_template("index.html")

@app.route('/<page>')
def static_route(page):
    if(page == "add_result"):
        return ""
    
    return render_template(page)

# static routes - dynamic pages #

@app.route('/add_result', methods = ['POST'])
def result():
    form = request.form
    try:
        title = str(form['title'])

        if(os.path.exists("./recipes/" + title + ".json")):
            return "Error: Recipe already exists"
        #endif

        recipe_json = json.loads(json.dumps(form))

        if(not (str(form['image']).startswith("h"))):
            recipe_json['image'] = None

        if(len(str(form['cook_time'])) < 1):
            recipe_json['None'] = None

        if(len(str(form['servings'])) < 1):
            recipe_json['servings'] = None
        
        if(len(str(form['calories_per_serving'])) < 1):
            recipe_json['calories_per_serving'] = None

        if(len(str(form['ingredients'])) < 1):
            recipe_json['ingredients'] = None
        else:
            recipe_json['ingredients'] = str(form['ingredients']).split(',')
        #end else

        directions = str(form['directions']).replace('\n','')

        if(len(str(form['references'])) < 1):
            recipe_json['references'] = None
            print("no references")
        else:
            references_raw = form['references'].split(',')
            print("references_raw: " + str(references_raw))
            references = list()
            for reference_raw in references_raw:
                reference_split = reference_raw.split(':', 1)
                print("reference_split: " + str(reference_split))
                if(len(reference_split) != 2): continue

                reference = dict()
                reference['name'] = reference_split[0]
                reference['link'] = reference_split[1]
                references.append(reference)
            #endfor
            recipe_json['references'] = references

        if(len(str(form['tags'])) < 1):
            recipe_json['tags'] = None
        else:
            recipe_json['tags'] = str(form['tags']).split(',')
        #endif
        
        recipe_json_str = json.dumps(recipe_json)
        print(recipe_json_str)
        
        output_file = open("./recipes/" + title + ".json","w")
        output_file.write(recipe_json_str)
        return build_html(recipe_json)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

        return 'Internal error: ' + str(e)

    return 'success'
#end

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