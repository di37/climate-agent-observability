"""Database query tools for SQL execution."""

import sqlite3
import logging
from agno.tools import tool
from ..config.settings import DB_FILE

logger = logging.getLogger(__name__)


@tool
def query_database(sql: str) -> str:
    """
    Execute a SQL query on the climate_agriculture_data database.
    
    Args:
        sql: The SQL query to execute (SELECT statements only)
    
    Returns:
        Query results as a formatted string
    """
    try:
        logger.debug(f"Executing SQL query: {sql[:100]}...")
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        conn.close()
        
        if not results:
            logger.info("Query returned no results")
            return "No results found."
        
        # Format results
        output = f"Query returned {len(results)} rows:\n\n"
        output += " | ".join(column_names) + "\n"
        output += "-" * 80 + "\n"
        
        for row in results[:20]:
            output += " | ".join(str(val) for val in row) + "\n"
        
        if len(results) > 20:
            output += f"\n... and {len(results) - 20} more rows"
        
        logger.info(f"Query executed successfully, returned {len(results)} rows")
        return output
        
    except Exception as e:
        logger.error(f"SQL execution error: {e}")
        return f"Error executing query: {str(e)}"

