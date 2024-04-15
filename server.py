import pyodbc

# Connect to your database
connection = pyodbc.connect('DRIVER={YourDriver};SERVER=YourServer;DATABASE=YourDatabase;UID=YourUsername;PWD=YourPassword')

# Function to fetch distinct dataset names and dataset definition IDs and store them in a dictionary
def fetch_dataset_info():
    dataset_info = {}
    
    # Fetch distinct dataset names
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT dataset_name FROM YourTable1 WHERE condition = 'YourCondition'")
    dataset_names = [row.dataset_name for row in cursor.fetchall()]
    
    # Fetch distinct dataset definition IDs for each dataset name
    for dataset_name in dataset_names:
        cursor.execute("SELECT DISTINCT dataset_definition_id FROM YourTable2 WHERE dataset_name = ? AND condition = 'YourCondition'", (dataset_name,))
        dataset_definition_ids = [row.dataset_definition_id for row in cursor.fetchall()]
        dataset_info[dataset_name] = dataset_definition_ids
    
    cursor.close()
    return dataset_info

# Function to retrieve attributes for a given dataset definition ID
def get_attributes(dataset_definition_id):
    cursor = connection.cursor()
    cursor.execute("SELECT attribute_name, attribute_datatype FROM YourTable3 WHERE dataset_definition_id = ?", (dataset_definition_id,))
    attributes = cursor.fetchall()
    cursor.close()
    return attributes

# Function to format the attributes
def format_attributes(attributes):
    formatted_result = ""
    for attribute in attributes:
        formatted_result += f"{attribute.attribute_name} {attribute.attribute_datatype},\n"
    return formatted_result

# Function to get attributes for a given dataset name
def get_and_format_data(dataset_name):
    # Fetch dataset definition IDs for the given dataset name from the dictionary
    dataset_info = fetch_dataset_info()
    dataset_definition_ids = dataset_info.get(dataset_name)
    if not dataset_definition_ids:
        return "Dataset name not found."
    
    # Fetch and format attributes for each dataset definition ID
    formatted_result = ""
    for dataset_definition_id in dataset_definition_ids:
        attributes = get_attributes(dataset_definition_id)
        formatted_result += format_attributes(attributes)
    
    return formatted_result

# Example usage
result = get_and_format_data(dataset_name="YourDatasetName")
print(result)
