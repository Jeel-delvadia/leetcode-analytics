# Chrome Extension Guide — Local Development & Store Publishing

This guide explains how to run the LeetCode Collector Chrome Extension locally and publish it to the Chrome Web Store.

---

## 1. Running the Extension Locally (Developer Mode)

### Step 1: Load Unpacked Extension into Chrome
1. Open Google Chrome.
2. In the address bar, navigate to: `chrome://extensions/`
3. In the top-right corner, turn **ON** **Developer mode**.
4. Click the **Load unpacked** button in the top-left menu.
5. Select the `extension` directory from your repository:
   `D:\lc\leetcode-analytics\extension`

### Step 2: Start the FastAPI Backend Server
Before syncing data from the extension, ensure the backend API server is running:

```bash
# In leetcode-analytics directory:
venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```
Backend API will be running at `http://localhost:8000`.

### Step 3: Trigger Synchronization
1. Open Chrome and log into your account at `https://leetcode.com`.
2. Click the puzzle icon (Extensions) in Chrome's top toolbar and pin **LeetCode Analytics**.
3. Click the extension icon to open the popup.
4. Click **Trigger Full Sync** to collect problem metadata and contest history.

---

## 2. Publishing to the Chrome Web Store

### Step 1: Package Extension into a ZIP File
Zip the contents of the `extension/` directory (ensure `manifest.json` is at the root of the `.zip` archive):

- **Files to include**: `manifest.json`, `popup.html`, `popup.js`, `src/` folder.

### Step 2: Register Chrome Web Store Developer Account
1. Visit the [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/devconsole).
2. Sign in with your Google Account.
3. Pay the one-time $5 USD registration fee required by Google for publishing extensions.

### Step 3: Create New Item Listing
1. In the Developer Dashboard, click **Add new item**.
2. Upload your `extension.zip` file.
3. Fill in the store listing metadata:
   - **Title**: LeetCode Personal Analytics Collector
   - **Summary**: Automatically collects LeetCode problem progress and contest history for personal analytics.
   - **Detailed Description**: Explain features, permissions, and single-purpose utility.
   - **Category**: Developer Tools / Productivity.
   - **Icon**: Upload 128x128 PNG icon.
   - **Screenshots**: Upload at least one 1280x800 or 640x400 screenshot showing the popup UI.

### Step 4: Privacy & Permissions Justification
1. Under **Privacy Practices**:
   - State that data is processed locally for personal analytics.
   - Single-Purpose Justification: "Intercepts user LeetCode submissions to record performance statistics."
   - Declare host permissions (`https://leetcode.com/*`).

### Step 5: Submit for Review
1. Click **Submit for review**.
2. Automated & manual review by Google typically takes 24–48 hours. Once approved, the extension goes live!
