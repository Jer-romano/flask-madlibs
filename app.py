from flask import Flask, request, render_template, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import re
from stories import Story, example_story

app = Flask(__name__)
app.config["SECRET_KEY"] = "My super secret key" 

debug = DebugToolbarExtension(app)

@app.route("/")
def home_page():
    '''Displays the home page, where user decides what type of story they'd like to use'''
    return render_template("home.html")

@app.route("/form")
def add_prompt_form():
    '''Displays form where user can input their answers'''
    story_string = request.args.get("story_input")
    if story_string:
        prompts_list = re.findall(r'\{(\w+)\}', story_string)
        story = Story(prompts_list, story_string)
    elif request.args.get("preset-story"):
        story = example_story
    else: #if user selects nothing, just go back to home page
        return render_template("home.html")

    session["story"] = story.__dict__  #__dict__ method converts Story object to JSON
    return render_template("form.html", story=story)

@app.route("/story")
def submit_prompts():
    '''Displays finished story'''
    story = Story(session["story"].get("prompts"), session["story"].get("template"))
    text = story.generate(request.args)
    return render_template("story.html", story=text)


