# AI-Mongo-Agent

A project for AI-powered MongoDB agent with Streamlit frontend.

## Description

This repository contains the implementation of an AI-powered MongoDB agent with a Streamlit-based user interface for authentication and interaction.

## Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/surya-sukumar/AI-Mongo-Agent.git
   cd AI-Mongo-Agent
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up MongoDB:

   - Make sure MongoDB is installed and running locally
   - Create a `.env` file based on `.env.example`
   - Update the MongoDB connection string in `.env` if needed

4. Run the application:
   ```bash
   streamlit run src/app.py
   ```

## Features

- User Authentication
  - Login
  - Registration
  - Password encryption
- MongoDB Integration
- Streamlit UI

## Project Structure

```
.
├── config/
│   └── config.py         # Configuration settings
├── src/
│   ├── app.py           # Main Streamlit application
│   ├── database.py      # Database operations
│   └── pages/           # Additional pages
├── requirements.txt     # Project dependencies
└── README.md           # Project documentation
```
