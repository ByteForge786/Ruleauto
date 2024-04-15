 import pyodbc

# Connect to your database
connection = pyodbc.connect('DRIVER={YourDriver};SERVER=YourServer;DATABASE=YourDatabase;UID=YourUsername;PWD=YourPassword')

# Global variables for caching results
dataset_cache = {}

# Function to retrieve dataset names from the first query
def get_dataset_names():
    sql_query = "SELECT DISTINCT dataset_name FROM YourTable1 WHERE condition = 'YourCondition'"
    cursor = connection.cursor()
    cursor.execute(sql_query)
    dataset_names = [row.dataset_name for row in cursor.fetchall()]
    cursor.close()
    return dataset_names

# Function to retrieve dataset definition IDs from the second query
def get_dataset_definition_ids(dataset_name):
    sql_query = "SELECT dataset_definition_id FROM YourTable2 WHERE dataset_name = ? AND condition = 'YourCondition'"
    cursor = connection.cursor()
    cursor.execute(sql_query, (dataset_name,))
    dataset_definition_ids = [row.dataset_definition_id for row in cursor.fetchall()]
    cursor.close()
    return dataset_definition_ids

# Function to retrieve attributes for each dataset definition ID
def get_attributes(dataset_definition_ids):
    attributes = []
    for dataset_definition_id in dataset_definition_ids:
        sql_query = """
            SELECT attribute_name, attribute_datatype
            FROM YourTable3
            WHERE dataset_definition_id = ? 
        """
        cursor = connection.cursor()
        cursor.execute(sql_query, (dataset_definition_id,))
        attributes.extend(cursor.fetchall())
        cursor.close()
    return attributes

# Function to retrieve data either from cache or pyodbc
def get_data(dataset_name):
    global dataset_cache
    
    # Check if data is in cache
    if dataset_name in dataset_cache:
        return dataset_cache[dataset_name]
    else:
        # Execute SQL queries
        dataset_names = get_dataset_names()
        dataset_definition_ids = get_dataset_definition_ids(dataset_name)
        attributes = get_attributes(dataset_definition_ids)
        
        # Update cache
        dataset_cache[dataset_name] = (dataset_names, dataset_definition_ids, attributes)
    
    return dataset_cache[dataset_name]

# Function to format the result
def format_result(dataset_names, dataset_definition_ids, attributes):
    formatted_result = ""
    for dataset_name in dataset_names:
        formatted_result += f"{dataset_name}\n"
        for dataset_definition_id in dataset_definition_ids:
            formatted_result += f"{dataset_definition_id}\n"
        for attribute in attributes:
            formatted_result += f"{attribute.attribute_name} {attribute.attribute_datatype}\n"
    
    return formatted_result

# Example usage
def get_and_format_data(dataset_name):
    dataset_names, dataset_definition_ids, attributes = get_data(dataset_name)
    return format_result(dataset_names, dataset_definition_ids, attributes)

result = get_and_format_data(dataset_name="YourDatasetName")
print(result)
