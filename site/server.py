import os
import json
from flask import Flask
from flask import render_template
from build_html import build_html
from build_html import parse_file

app = Flask(__name__)

# static routes #

@app.route('/')
def root(): return render_template("index.html")

@app.route('/index.html')
def index(): return render_template("index.html")

@app.route('/edit.html')
def edit(): return render_template("edit.html")

@app.route('/new_recipe.html')
def new_recipe(): return render_template("new_recipe.html")

# static routes - dynamic pages #

@app.route('/recipes.html')
def recipes():
    return_html = ''

    directory = os.fsencode("./recipes")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json"): 
            filename = filename.replace('.json','')
            return_html = str(filename)
        #endif
    #endfor

    return return_html
# end recipes()

# dynamic routes - dynamic pages #

@app.route('/recipes/<page>')
def recipe(page):
    input_json = parse_file('./recipes/' + page.replace('.html','.json'))
    if(input_json == None): return "recipe not found or corrupted"

    return build_html(input_json)
#end recipe()

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', threaded=True)