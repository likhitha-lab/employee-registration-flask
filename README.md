# Employee Registration Form (Flask)

Flask web application for Computer Use Agent testing. It serves a single form page with a double-click interaction. There is no database; everything happens in the browser and nothing is stored or sent anywhere.

## Project structure

```
app.py                Flask app: GET / (form) and GET /health
requirements.txt      Flask and gunicorn
Procfile              Start command for Railway (and other Procfile-based hosts)
templates/index.html  Form markup
static/styles.css     Styles with purple accents
static/app.js         Double-click, keyboard and submit behavior
.gitignore
README.md
```

## Behavior

| Action | Result |
|--------|--------|
| Page load | Additional Details hidden. Submit disabled. |
| Single click on "Review your information" | Nothing happens. |
| Double-click on "Review your information" | Additional Details (Location, Comments) appears, "Review section opened successfully." is displayed, the section turns green, Submit is enabled. |
| Tab to the review section, press Enter or Space | Same as double-click. |
| Click Submit (after review is opened) | "Form submitted successfully." is displayed. No network request is made. |

Fields are not validated; the review section opens even when fields are empty.

## Test IDs

| data-testid | Element |
|-------------|---------|
| `full-name` | Full Name input |
| `work-email` | Work Email input |
| `department` | Department select (Engineering, Finance, Marketing, HR) |
| `review-section` | Review your information section |
| `review-success` | "Review section opened successfully." (in the DOM, hidden until opened) |
| `submit-button` | Submit button |
| `submit-success` | "Form submitted successfully." (in the DOM, hidden until submitted) |

The two success messages always exist in the DOM with the `hidden` attribute. Test for visibility, not presence.

## Run locally

Requires Python 3.10 or later.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Open http://localhost:8080. The server listens on `0.0.0.0` and uses the `PORT` environment variable, defaulting to `8080`:

```bash
PORT=5000 python app.py          # macOS / Linux
$env:PORT=5000; python app.py    # Windows PowerShell
```

Production-style run on macOS or Linux (gunicorn does not run on Windows):

```bash
PORT=8080 gunicorn --bind 0.0.0.0:$PORT app:app
```

Health check: `GET /health` returns `{"application": "employee-registration-flask", "status": "ok"}`.

## Deploy

Push this folder to a GitHub repository first (as the repository root, or set the root directory to this folder on each platform).

### Render

1. In the Render dashboard, select **New > Web Service** and connect the repository.
2. Settings:
   - **Runtime**: Python 3
   - **Root Directory**: blank, or `employee-registration-flask` if it is a subfolder
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`
   - **Health Check Path** (Advanced): `/health`
3. Select **Create Web Service**. Render sets `PORT` automatically.

### Railway

1. In Railway, select **New Project > Deploy from GitHub repo** and choose the repository.
2. If the app is in a subfolder, set **Settings > Source > Root Directory** to `employee-registration-flask`.
3. Railway detects Python from `requirements.txt` and uses the `Procfile` start command. `PORT` is injected automatically.
4. Under **Settings > Networking**, select **Generate Domain** to get a public URL.
5. Optional: set **Settings > Deploy > Healthcheck Path** to `/health`.

### Azure App Service (Linux)

Using the Azure CLI from this folder:

```bash
az login
az webapp up --name <unique-app-name> --resource-group <resource-group> --runtime "PYTHON:3.12" --sku B1
```

`az webapp up` creates the App Service plan and web app if needed, uploads the code and builds it with `requirements.txt`.

Then set the startup command:

```bash
az webapp config set --name <unique-app-name> --resource-group <resource-group> \
  --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 app:app"
```

Notes:
- Azure ignores the `Procfile`. Without a startup command, App Service also detects `app.py` and runs gunicorn automatically.
- App Service for Python expects the app on port 8000, which is gunicorn's default when no port is given, so the startup command above does not use `$PORT`.
- Alternatively, deploy from GitHub in the portal: **Web App > Deployment Center > GitHub**, then set **Configuration > General settings > Startup Command** to the command above.
- Open `https://<unique-app-name>.azurewebsites.net/health` to verify.

## Test cases for a Computer Use Agent

| ID | Instruction to the agent | Expected result |
|----|--------------------------|-----------------|
| CUA-01 | Open the page and describe the form. | Title "Employee Registration Form" with Full Name, Work Email, Department. Submit disabled. |
| CUA-02 | Fill Full Name, Work Email and select a department. | Values appear in the fields. |
| CUA-03 | Click the "Review your information" section once. | Nothing changes. |
| CUA-04 | Double-click the "Review your information" section. | "Review section opened successfully." appears, Location and Comments appear, Submit is enabled. |
| CUA-05 | Reload, fill the fields, press Tab until the review section is focused, press Enter. | Same result as CUA-04. |
| CUA-06 | Reload, focus the review section, press Space. | Same result as CUA-04. The page does not scroll. |
| CUA-07 | Fill Location and Comments, click Submit. | "Form submitted successfully." appears. |
| CUA-08 | Reload and try to click Submit before opening the review section. | Submit is disabled and nothing happens. |
