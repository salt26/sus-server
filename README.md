# How to start

## Development mode

<pre><code>venv\Scripts\activate
set FLASK_APP=sus.py
flask run
</code></pre>

## Deployment mode

<pre><code>venv\Scripts\activate
set PYTHONPATH=.
twistd web --port tcp:8000 --wsgi sus.app
</code></pre>