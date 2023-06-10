from flask import Flask, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
import re
from stories import Story, example_story

app = Flask(__name__)
app.config["SECRET_KEY"] = "My super secret key" 

debug = DebugToolbarExtension(app)
story_list = []

@app.route("/")
def home_page():
    '''Displays the home page'''
    return render_template("home.html")

@app.route("/form")
def add_prompt_form():
    '''Displays form where user can input their answers'''
    story_string = request.args.get("story_input")
    if story_string:
        prompts_list = re.findall(r'\{(\w+)\}', story_string)
        story = Story(prompts_list, story_string)
    else:
        story = example_story
    
    return render_template("form.html", story=story)

@app.route("/story")
def submit_prompts():
    '''Displays finished story'''
    text = example_story.generate(request.args)
    #text = story.
    return render_template("story.html", story=text)

# @app.route("/story/<story_obj>")
# def show_story(story_obj):
#     s = story_list[0]
#     return render_template("story.html", story=s)
