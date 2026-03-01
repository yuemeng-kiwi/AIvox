# Deployment Guide: Omotenashi Care

Currently, your app is running **locally** on your machine. To share it with the world, the best platform for Streamlit apps is **Streamlit Community Cloud**.

## Prerequisites
I have already prepared the necessary files for you:
- [x] `app.py` (Main application)
- [x] `requirements.txt` (Dependencies)
- [x] `config.py` (Configuration)

## Step-by-Step Deployment

### 1. Push to GitHub
You need to push this project to a public GitHub repository.
1. Create a new repository on GitHub.
2. Run these commands in your terminal (replace `<your-repo-url>`):
   ```bash
   git init
   git add .
   git commit -m "Initial commit of Omotenashi Care"
   git branch -M main
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

### 2. Deploy on Streamlit Community Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io/).
2. Click **"New app"**.
3. Select your GitHub repository (`omotenashi-care`).
4. Set the **Main file path** to: `omotenashi-care/app.py`
5. Click **"Deploy!"**.

### 3. Configure Secrets (For Phase 2)
Once you get your real API keys for MiniMax and Agora, go to your app's **Settings > Secrets** on Streamlit Cloud and add them:

```toml
MINIMAX_API_KEY = "your_key_here"
AGORA_APP_ID = "your_id_here"
```

Your app will then be live and accessible via a public URL!
