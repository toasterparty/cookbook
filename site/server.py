import json
from flask import Flask
from flask import render_template
from build_html import build_html

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

# dynamic routes #

@app.route('/recipes/<page>')
def recipe(page):
    try:
        input_file = open('recipes/' + page.replace('.html','.json'), 'r')
    except Exception:
        print("recipe not found")
        return "recipe not found"
    #end try/except
    
    try:
        input_json = json.load(input_file)
        input_file.close()
    except Exception:
        print("Failed to parse input json")
        input_file.close()
        return "invalid recipe data record"
    #end try/except

    return build_html(input_json)

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', threaded=True)
