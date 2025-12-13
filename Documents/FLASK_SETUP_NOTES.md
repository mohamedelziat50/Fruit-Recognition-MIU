# Flask Setup Notes

## Project Structure
Flask requires a specific directory structure for templates and static files:

```
Fruit-Recognition-MIU/
├── app.py                 # Flask application (root level)
├── templates/            # HTML templates (Flask convention)
│   └── index.html
├── static/               # Static files (CSS, JS, images) - Flask convention
│   ├── styles.css
│   ├── script.js
│   └── images/
│       ├── favicon.ico
│       ├── fruity-detect-logo.png
│       ├── fruit-bowl.png
│       ├── all-fruits.png
│       └── fruit-recognition-pipeline.png
└── requirements.txt
```

## Key Points

### 1. Static Files Location
- **Flask automatically serves files from `static/` folder**
- Static files (CSS, JS, images) MUST be in the root `static/` directory
- Flask serves them at `/static/` URL path automatically

### 2. Templates Location
- HTML templates go in `templates/` folder
- Flask looks for templates in `templates/` by default
- Use `render_template("file.html")` to render templates

### 3. Referencing Static Files in HTML
Always use Flask's `url_for()` function in templates:

```html
<!-- CSS -->
<link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">

<!-- JavaScript -->
<script src="{{ url_for('static', filename='script.js') }}"></script>

<!-- Images -->
<img src="{{ url_for('static', filename='images/logo.png') }}" alt="Logo">
```

**Why?** `url_for()` generates the correct URL path (`/static/...`) that Flask can serve, regardless of deployment environment.

### 4. Flask App Initialization
```python
from flask import Flask

# Correct - use __name__ (variable), not '__name__' (string)
app = Flask(__name__)

# Flask automatically knows:
# - Templates are in 'templates/' folder
# - Static files are in 'static/' folder
```

### 5. Common Mistakes to Avoid

❌ **DON'T:**
- Put static files in `templates/` folder
- Use relative paths like `href="styles.css"` in templates
- Put HTML files in `static/` folder
- Use `Flask('__name__')` with quotes

✅ **DO:**
- Put static files in root `static/` folder
- Use `url_for('static', filename='...')` in templates
- Put HTML templates in `templates/` folder
- Use `Flask(__name__)` without quotes

## Testing Static Files

After setting up, check browser console and Flask logs:
- ✅ `200` status = file loaded successfully
- ❌ `404` status = file not found (check path and location)

Example successful Flask log:
```
127.0.0.1 - - [13/Dec/2025 16:06:18] "GET /static/styles.css HTTP/1.1" 200 -
127.0.0.1 - - [13/Dec/2025 16:06:18] "GET /static/script.js HTTP/1.1" 200 -
127.0.0.1 - - [13/Dec/2025 16:06:18] "GET /static/images/logo.png HTTP/1.1" 200 -
```

## Quick Reference

| File Type | Location | How to Reference in HTML |
|-----------|----------|-------------------------|
| HTML templates | `templates/` | `render_template("index.html")` |
| CSS files | `static/` | `{{ url_for('static', filename='styles.css') }}` |
| JavaScript | `static/` | `{{ url_for('static', filename='script.js') }}` |
| Images | `static/images/` | `{{ url_for('static', filename='images/logo.png') }}` |

## Notes
- Flask's static file serving is automatic - no route configuration needed
- The `static/` folder name is a Flask convention, not configurable by default
- `url_for()` is the recommended way to generate URLs in Flask templates

