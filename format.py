def format_file():
    # Get filename from user
    filename = input("Enter the filename (with .txt): ")
    
    try:
        # Read the file content
        with open(filename, 'r') as file:
            content = file.read()
        
        # Split by comma and clean each item
        items = [item.strip() for item in content.split(',') if item.strip()]
        
        # Write back to the same file with new format
        with open(filename, 'w') as file:
            file.write('\n'.join(items))
            
        print(f"File {filename} has been formatted successfully!")
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    format_file()
