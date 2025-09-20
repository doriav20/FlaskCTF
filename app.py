import os
import random

from flask import Flask, redirect, render_template, request
from werkzeug.debug import get_pin_and_cookie_name

from constants import PIN_FILE, SECRET_DIR, UPLOADS_DIR
from utils import get_random_filename, is_admin, obfuscate_string

app = Flask(__name__)


def render_base_page(title: str = "", content: str = "", status_code: int = 200):
    """
    Render a base page with a title, content, and status code.

    Parameters
    ----------
    title : str
        The title of the page.
    content : str
        The main content of the page.
    status_code : int
        The HTTP status code to return.

    Returns
    -------
    tuple[str, int]
        A tuple containing the rendered HTML and the status code.
    """

    return render_template('base_page.html', title=title, content=content, status_code=status_code), status_code


@app.route('/')
def index():
    """
    Render the main page with a form to upload stories and a list of existing stories.

    This page also includes a form to get a random story, optionally filtered by name.
    """

    stories = os.listdir(UPLOADS_DIR)
    stories = [s for s in stories if s.startswith('story_')]

    # Render index.html stored in the "templates" directory.
    return render_template('index.html', stories=stories)


@app.route('/stories', methods=['POST'])
def upload_story():
    """
    Handle the story upload from the form submission.
    This endpoint expects a POST request with a 'story' parameter.

    If the upload is successful, it saves the story to a file with a random name and returns a link to view the uploaded story.
    If the 'story' parameter is missing, it returns a 400 error.
    """

    story = request.form.get('story')
    if not story:
        return render_base_page("Error", "Please provide a 'story' parameter.", 400)

    random_filename = 'story_' + get_random_filename(16, 'txt')

    file_path = os.path.join(UPLOADS_DIR, random_filename)
    with open(file_path, 'w', encoding='utf-8') as story_file:
        story_file.write(story)

    return render_template('upload_success.html', filename=random_filename)


@app.route('/stories/view')
def view_story():
    filename = request.args.get('filename')
    if not filename:
        return render_base_page("Error", "Please provide a 'filename' parameter.", 400)

    story_path = os.path.join(UPLOADS_DIR, filename)
    if not os.path.isfile(story_path):
        return render_base_page("Error", f"{filename} not found.", 404)

    try:
        with open(story_path, 'r', encoding='utf-8') as f:
            story_content = f.read()
    except:
        return render_base_page("Error", f"Error reading {filename}", 500)

    return render_base_page(filename, story_content)


@app.route('/random_story', methods=['GET'])
def get_random_story():
    """
    Get random story and get optional filter parameter to filter by name

    This endpoint retrieves a random story from the uploads directory.
    If a filter parameter is provided, it filters the stories by the given name.
    """
    filter_name = request.args.get('filter')
    stories = os.listdir(UPLOADS_DIR)

    if filter_name:
        stories = [s for s in stories if filter_name in s]

    random.shuffle(stories)
    random_story = stories[0]

    return redirect(f'/stories/view?filename={random_story}')


@app.route('/admin_dashboard', methods=['GET'])
def admin_dashboard():
    """
    Render the admin dashboard page.
    This page is only accessible to admins.
    """

    username = request.args.get('username')
    if not username:
        return render_base_page("Error", "Please provide a 'username' parameter.", 400)

    is_user_admin = is_admin(username)
    if not is_user_admin:
        return render_base_page("Error", "You are not an admin.", 403)

    return render_base_page("Admin Dashboard", f"Welcome to the admin dashboard, {username}!")


if __name__ == '__main__':
    print("Story Fun starting up...")

    os.makedirs(UPLOADS_DIR, exist_ok=True)
    os.makedirs(SECRET_DIR, exist_ok=True)

    debug_pin, _ = get_pin_and_cookie_name(app)
    obfuscated_pin = obfuscate_string(debug_pin)
    with open(PIN_FILE, 'w', encoding='utf-8') as f:
        f.write(obfuscated_pin)

    app.run(host='0.0.0.0', port=5000, debug=True)
