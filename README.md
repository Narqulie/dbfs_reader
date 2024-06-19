
# Databricks DBFS File Navigator

This script allows you to navigate Databricks DBFS, preview file contents, and download files to your local machine. It uses Databricks REST API to interact with DBFS.

## Features

- List files and directories in a given DBFS path.
- Preview contents of CSV files stored in DBFS.
- Download files from DBFS to your local machine.

## Requirements

- Python 3.7 or higher
- `requests` library
- `python-dotenv` library
- `polars` library

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/databricks-dbfs-navigator.git
   cd databricks-dbfs-navigator
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scriptsctivate`
   ```

3. **Install the required libraries:**
   ```bash
   pip install requests python-dotenv polars
   ```

4. **Create a `.env` file in the project directory and add your Databricks access token and instance URL:**
   ```env
   DATABRICKS_ACCESS_TOKEN=your-access-token
   DATABRICKS_INSTANCE=https://your-databricks-instance
   ```

## Usage

Run the script:
```bash
python dbfs_navigator.py
```

The script will prompt you to navigate through the directories and files in DBFS. You can:

- Enter a number to navigate into a directory or preview a file.
- Enter `..` to go up one directory level.
- Enter `exit` to quit the script.

### Example Interaction

```
Listing contents of dbfs:/:

1. Directory: dbfs:/my-directory
2. File: dbfs:/my-file.csv (Size: 1024 bytes)

Enter the number to navigate into (or '..' to go up, 'exit' to quit): 1

Listing contents of dbfs:/my-directory/:

1. File: dbfs:/my-directory/another-file.csv (Size: 2048 bytes)

Enter the number to navigate into (or '..' to go up, 'exit' to quit): 1

File dbfs:/my-directory/another-file.csv content:

shape: (3, 2)
┌──────────┬──────────┐
│ column_1 │ column_2 │
│ ---      │ ---      │
│ str      │ str      │
╞══════════╪══════════╡
│ value1   │ value2   │
│ value3   │ value4   │
│ value5   │ value6   │
└──────────┴──────────┘

Do you want to download this file? (yes/no): yes
File dbfs:/my-directory/another-file.csv downloaded successfully to /path/to/your/project/downloaded/another-file.csv.
```


## Acknowledgements

- [Databricks API Documentation](https://docs.databricks.com/dev-tools/api/latest/index.html)
