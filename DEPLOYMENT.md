# Deploying to Netlify

## Quick Deploy Steps

1. **Create a GitHub repository** (if you haven't already):
   - Go to GitHub and create a new repository
   - Push your code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy to Netlify**:
   - Go to [netlify.com](https://www.netlify.com/)
   - Sign up or log in
   - Click "Add new site" → "Import an existing project"
   - Connect to GitHub and select your repository
   - Netlify will auto-detect settings from `netlify.toml`
   - Click "Deploy site"

3. **Your site will be live!**
   - Netlify will give you a URL like: `https://your-site-name.netlify.app`
   - You can customize the domain name in site settings

## Alternative: Drag & Drop Deploy

1. Go to [netlify.com/drop](https://app.netlify.com/drop)
2. Drag and drop these files:
   - index.html
   - styles.css
   - script.js
   - netlify.toml
3. Your site goes live instantly!

## Important Notes

- This version uses **localStorage** for data storage (browser-based)
- Data is stored locally in each user's browser
- For a production app with shared database, you'd need a backend service
- The Flask version (app.py) can be deployed to platforms like:
  - Heroku
  - Railway
  - Render
  - PythonAnywhere

## Testing Locally

Simply open `index.html` in your browser, or use:
```bash
python -m http.server 8000
```
Then visit: `http://localhost:8000`
