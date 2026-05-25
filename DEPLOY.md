# Deployment Guide

This guide provides step-by-step instructions to deploy the CryptoTax-DE application. Because this is a Streamlit application, the recommended hosting platform is [Streamlit Community Cloud](https://streamlit.io/cloud).

## Deploying to Streamlit Community Cloud

1. **Push your code to GitHub:** Ensure your repository containing `app.py`, `requirements.txt`, and `src/` is pushed to a public or private GitHub repository.
2. **Log in to Streamlit:** Go to [share.streamlit.io](https://share.streamlit.io) and log in with your GitHub account.
3. **Create a new app:** Click the **"New app"** button.
4. **Configure the app:**
   - **Repository:** Select your GitHub repository.
   - **Branch:** Select the branch (e.g., `main` or `feat/mvp-implementation`).
   - **Main file path:** Enter `app.py`.
5. **Advanced Settings (Environment Variables):**
   - Click on **"Advanced settings"** before deploying.
   - Under the "Secrets" field (which acts as environment variables), you can specify variables. For the current MVP, you can configure the mock flags for the test pipeline (though not strictly needed for the app itself):
     ```toml
     MOCK_LLM = "true"
     USE_MOCK_MODEL = "true"
     MOCK_DATA = "true"
     ```
6. **Deploy!** Click the **"Deploy!"** button. Streamlit will automatically read your `requirements.txt`, install the dependencies, and launch your application.

## Environment Variables / Secrets Reference

The following environment variables are recognized by the application's test / CI suite:

| Variable | Description |
|---|---|
| `MOCK_LLM` | Set to `true` to mock LLM interactions (if implemented in future). |
| `USE_MOCK_MODEL` | Set to `true` to use mock models instead of real endpoints. |
| `MOCK_DATA` | Set to `true` to utilize mock/sample data without requiring user CSV uploads. |

*(Note: The current MVP operates entirely locally without external APIs, so these variables are primarily utilized for CI pipeline parity as requested.)*
