import pandas as pd
import sqlite3
from langchain.tools import tool

@tool
def get_expense_value(country):
    """
    Use this tool ONLY when the user asks for the expenses of the company for a specific
    country. Do not use this tool if the user is asking about multiple countries.
    """
    print("The agent is using get_expense_value tool")

    data = pd.read_csv("tool_files/The Keepsake expenses.csv")

    if country not in data['country'].values:
        return f"Invalid country name {country}"

    value = data.loc[data['country'] == country, 'expenses']

    return float(value.iloc[0])

@tool
def combine_expenses(country1, country2):
    """
    Use this tool ONLY when asked to combine expenses for EXACTLY two countries.
    ALWAYS use this tool when asked to add expenses for two countries.
    """

    print("The agent is using combine_expenses tool")

    data = pd.read_csv("tool_files/The Keepsake expenses.csv")

    if country1 not in data['country'].values:
        return f"Invalid country name {country1}"

    if country2 not in data['country'].values:
        return f"Invalid country name {country2}"

    value1 = data.loc[data['country'] == country1, 'expenses']
    value2 = data.loc[data['country'] == country2, 'expenses']

    return float(value1.iloc[0]) + float(value2.iloc[0])

# What was the total revenue?

@tool
def query_transactions(sql_query: str):
    """
    Use this tool when the user asks questions that require querying transaction data.
    The tool executes a SQLite query on the company database and returns the results.
    The database has one table called raw_transactions with these columns:
    - InvoiceNo (TEXT)
    - StockCode (TEXT)
    - Description (TEXT)
    - Quantity (INTEGER)
    - InvoiceDate (TIMESTAMP)
    - UnitPrice (REAL)
    - CustomerID (REAL)
    - Country (TEXT)
    - LineRevenue (REAL)
    Only SELECT queries are allowed.
    """
    print("The agent is using query_transactions tool")
    print(sql_query)

    # do not allow the agent to execute queries that don't start with SELECT
    if not sql_query.strip().upper().startswith("SELECT"):
        return "Only SELECT queries are allowed."

    # connect to the database
    conn = sqlite3.connect("tool_files/company.db")
    try:
        # execute the query and save the result as a dataframe
        df = pd.read_sql_query(sql_query, conn)
        return df.to_string(index=False)
    # if executing the query returns error this Exception code will
    # tell the LLM that the query was wrong but the Agent will not break
    except Exception as e:
        return f"Query error: {str(e)}"
    finally:
        conn.close() # close the connection to the database