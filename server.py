import pyodbc

# Connect to your database
connection = pyodbc.connect('DRIVER={YourDriver};SERVER=YourServer;DATABASE=YourDatabase;UID=YourUsername;PWD=YourPassword')

# Global variables for caching results
dataset_cache = {}

# Function to retrieve data either from cache or pyodbc
def get_data(dataset_name):
    global dataset_cache
    
    # Check if data is in cache
    if dataset_name in dataset_cache:
        return dataset_cache[dataset_name]
    else:
        # SQL queries
        sql_query_1 = "SELECT DISTINCT dataset_name FROM YourTable1 WHERE dataset_name = ? AND condition = 'YourCondition'"
        sql_query_2 = """
            SELECT dataset_definition_id
            FROM YourTable2
            WHERE dataset_name = ? AND dataset_definition_id IN (
                SELECT dataset_definition_id
                FROM YourTable2
                WHERE dataset_name = ? AND condition = 'YourCondition'
            )
        """
        sql_query_3 = """
            SELECT attribute_name, attribute_datatype
            FROM YourTable3
            WHERE dataset_definition_id IN (
                SELECT dataset_definition_id
                FROM YourTable2
                WHERE dataset_name = ? AND condition = 'YourCondition'
            )
        """
        
        # Execute SQL queries
        cursor = connection.cursor()
        
        # Execute SQL query 1
        cursor.execute(sql_query_1, (dataset_name,))
        dataset_names = [row.dataset_name for row in cursor.fetchall()]
        
        # Execute SQL query 2
        cursor.execute(sql_query_2, (dataset_name, dataset_name))
        dataset_definition_ids = [row.dataset_definition_id for row in cursor.fetchall()]
        
        # Execute SQL query 3
        cursor.execute(sql_query_3, (dataset_name,))
        attributes = cursor.fetchall()
        
        # Close cursor
        cursor.close()
        
        # Update cache
        dataset_cache[dataset_name] = (dataset_definition_ids, attributes)
    
    return dataset_cache[dataset_name]

# Function to format the result
def format_result(attributes):
    dataset_attributes = []
    for attribute in attributes:
        dataset_attributes.append(f"{attribute.attribute_name} {attribute.attribute_datatype}")
    
    formatted_attributes = ",\n".join(dataset_attributes)
    return formatted_attributes

# Example usage
def get_and_format_data(dataset_name):
    dataset_definition_ids, attributes = get_data(dataset_name)
    return format_result(attributes)

result = get_and_format_data(dataset_name="YourDatasetName")
print(result)
