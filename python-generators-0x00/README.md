# Python Generators - Streaming SQL Rows

## Objective

Create a generator that streams rows from a MySQL database one by one.

## Setup

1. Install dependencies:

```bash
   pip install mysql-connector-python
```

2. Ensure MySQL server is running and accessible from the workbench
3. Update MySQL in `seed.py`.
4. Run the main script

```bash
python 0-main.py
```

## Files

- `seed.py` - Database setup, insertion and generator functions
- `0-main.py` - Script to setup and display results
- `user_data.csv` - Sample data file

---

## Step 9. Verify in MySQL Workbench

After running the script:

1. Open **MySQL Workbench**

2. Connect to your local server
3. Run:

```sql
   USE ALX_prodev;
   SELECT * FROM user_data LIMIT 5;
```
