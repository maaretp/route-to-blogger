# route-to-blogger

Publish markdown posts (with images) to Blogger automatically on every push.

## How it works

1. Add a `.md` file under `posts/` (images go in the same folder).
2. Push to `main` — GitHub Actions converts the markdown to HTML, uploads images to Imgur, and creates or updates the Blogger post.
3. The generated post IDs are saved to `posts/.published.json` so future pushes update existing posts instead of creating duplicates.

## One-time setup

### 1. Google Cloud — Blogger API

1. Go to <https://console.cloud.google.com/> and create a project.
2. Enable the **Blogger API v3** for the project.
3. Create **OAuth 2.0 credentials** (type: _Desktop app_) and note the Client ID and Client Secret.

### 2. Obtain a refresh token

```bash
pip install google-auth-oauthlib
python get_refresh_token.py
```

Follow the browser prompt to authorise access to your Blogger account.  
The script prints the three values you need for the next step.

### 3. Google Drive — image hosting

No extra setup needed — the same OAuth2 credentials from step 1 are reused. The **Blogger API** project you created already covers this; just make sure the **Google Drive API** is also enabled for that project at <https://console.cloud.google.com/apis/library>.

### 4. GitHub repository secrets

Add these secrets under **Settings → Secrets and variables → Actions**:

| Secret                 | Value                       |
| ---------------------- | --------------------------- |
| `GOOGLE_CLIENT_ID`     | From step 2                 |
| `GOOGLE_CLIENT_SECRET` | From step 2                 |
| `GOOGLE_REFRESH_TOKEN` | From `get_refresh_token.py` |

## Post format

- The first `# Heading` in the file becomes the Blogger post title.
- Reference images with a standard markdown image tag; local files are uploaded automatically:
  ```markdown
  ![Alt text](picture.png)
  ```
