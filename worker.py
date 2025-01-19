import requests
from db import SessionLocal, store_operation_result

# Function to fetch the result from the API and store it in the database
def fetch_result_from_api_and_store(operation, num1, num2):
    # Construct the API URL for the operation
    api_url = f"http://127.0.0.1:8000/{operation}?num1={num1}&num2={num2}"

    try:
        # Make the API request
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for unsuccessful requests

        # Get the result from the response
        result_data = response.json()
        result = result_data.get("result")
        operation_id = result_data.get("id")

        # Open a session to the database and store the result
        db = SessionLocal()
        operation_record = store_operation_result(db, operation, num1, num2, result)
        db.close()

        return {
            "id": operation_record.id,
            "operation": operation,
            "num1": num1,
            "num2": num2,
            "result": result
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}

# Main function to simulate worker tasks
def main():
    # Example operations to test
    tasks = [
        ("sum", 25, 5),
        ("sub", 15, 7),
        ("mul", 3, 9),
        ("Div", 12, 4),
        ("Div", 10, 0)  # This will fail due to division by zero
    ]

    # Perform operations, fetch results from the API, and store them
    for operation, num1, num2 in tasks:
        result = fetch_result_from_api_and_store(operation, num1, num2)
        print(result)

if __name__ == "__main__":
    main()
