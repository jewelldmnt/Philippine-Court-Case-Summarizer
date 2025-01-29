# Philippine Court Case Summarizer

This project is designed to summarize Philippine court case documents. The system consists of three main modules: Preprocessing, Topic Segmentation, and Latent Semantic Analysis (LSA).

## Table of Contents

- [Overview](#overview)
- [Technologies Used](#technologies-used)
- [Screenshot of the UI](#screenshot-of-the-user-interface)
- [Installation](#installation)
- [Usage](#usage)

## Overview

The Philippine Court Case Summarizer processes court case documents and extracts meaningful segments to provide concise summaries. The system performs the following steps:

1. **Preprocessing**: Removing unnecessary characters and tokenization.
2. **Topic Segmentation**: Identifies and segments the document into coherent segments.
3. **Latent Semantic Analysis (LSA)**: Extracts the relevant sentences from the segmented text.

## Technologies Used

- **Backend**: Python, Flask  
  ![Python](https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg)  
  ![Flask](https://upload.wikimedia.org/wikipedia/commons/3/3c/Flask_logo.svg)

- **Frontend**: React.js  
  ![React](https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg)

- **Database**: SQLite  
  ![SQLite](https://upload.wikimedia.org/wikipedia/commons/3/38/SQLite370.svg)

## Screenshot of the User Interface


## Installation
1. Clone the repository:
 ```bash
git clone https://github.com/jewelldmnt/Philippine-Court-Case-Summarizer.git
cd Philippine-Court-Case-Summarizer
```
2. Install backend dependencies:
The `requirements.txt` file contains a list of required Python packages. Install these packages using the following command:
```bash
cd backend
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd ../frontend
npm install
```

## How to Run
To run the application, both the backend and frontend should be running:
1. Start the backend:
```bash
cd backend
python app.py
```

2. Start the frontend:
```bash
cd ../frontend
npm run dev
```
The application should now be running and accessible through the frontend.



