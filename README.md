# How to start

[How to set up your virtual environment](https://flask.palletsprojects.com/en/1.1.x/installation/)

## Development mode (Windows)

<pre><code>venv\Scripts\activate
set FLASK_APP=sus.py
flask run
</code></pre>

## Deployment mode (Windows)

<pre><code>venv\Scripts\activate
set PYTHONPATH=.
twistd web --port tcp:8000 --wsgi sus.app
</code></pre>
