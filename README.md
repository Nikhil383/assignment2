# Automated Data Query and Retrieval System

This project implements an automated data query and retrieval system using an open-source Large Language Model (LLM), Flask, MongoDB, LlamaIndex, and LangChain. It allows users to upload a CSV file, query the data using natural language, and retrieve results either as a displayed table or a downloadable CSV file. The system dynamically generates MongoDB queries based on user input using the `facebook/opt-125m` LLM.

## Project Overview
- **Objective**: Demonstrate the integration of LLMs with MongoDB for dynamic data querying and retrieval from CSV files.
- **Tools Used**:
  - **LLM**: `facebook/opt-125m` (125M parameters, ~500 MB memory footprint).
  - **Web Framework**: Flask for user interaction.
  - **Database**: MongoDB for storing and querying CSV data.
  - **Libraries**: LangChain, LlamaIndex, Transformers, PyMongo, Pandas.

## Prerequisites
- **Operating System**: Windows 10/11 (tested on 8 GB RAM system).
- **Python**: Version 3.8 or higher.
- **MongoDB**: Community Server installed and running locally.
- **Disk Space**: At least 2 GB free for dependencies and model files.
- **Internet**: Required for initial dependency and model downloads.

## Installation
1. **Install MongoDB**:
   - Download from [MongoDB Community Server](https://www.mongodb.com/try/download/community).
   - Install with default settings.
   - Create a data directory:
     ```cmd
     mkdir C:\data\db
  - Start MongoDb
    '''cmd
    mongod --dbpath C:\data\db
2. **Set Up Project**:
  - Place all project files (app.py, db_operations.py, query_generator.py, requirements.txt, sample_products.csv, and templates/ folder) in the directory.

## Running the Application
1. **Start MongoDB**:
   -In a cmd prompt:
   '''cmd
   mongod
2. ** Run the Flask APP**:
   '''cmd
   py app.py
## Usage
1.**Upload CSV**:
 - On the homepage, upload a CSV file (e.g., sample_products.csv).
 - The system loads the data into MongoDB and redirects to the query page.
2. **Query Data:**
 - Enter a natural language query (e.g., "Products with price > 50").
 - Optionally specify a test case name (e.g., test_case1).
 - Choose "Display" to see results in a table or "Save to CSV" to download them.
 - Submit the query.
3. **View Results:**
 - Display: Results appear in a table with a "Back" link to the homepage.
 - Save: Downloads a CSV file (e.g., test_case1.csv) to your system.

   
   
   
