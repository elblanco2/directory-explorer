import os
import sys

def get_dir_structure(root_dir, max_depth=float('inf'), ignore_patterns=None):
    """
    Recursively generate the directory structure.
    
    :param root_dir: Root directory path
    :param max_depth: Maximum depth of directory traversal
    :param ignore_patterns: List of patterns to ignore (e.g., ['.git', '__pycache__'])
    :return: Dictionary representing directory structure
    """
    if ignore_patterns is None:
        ignore_patterns = ['.git', '__pycache__', '.DS_Store']
    
    def _should_ignore(path):
        return any(pattern in path for pattern in ignore_patterns)
    
    def _explore(current_path, depth=0):
        # If depth exceeds max_depth, stop exploring
        if depth > max_depth:
            return {}
        
        structure = {}
        
        try:
            # List all items in the current directory
            for item in os.listdir(current_path):
                full_path = os.path.join(current_path, item)
                
                # Skip ignored patterns
                if _should_ignore(full_path):
                    continue
                
                if os.path.isdir(full_path):
                    # If it's a directory, recursively explore
                    structure[item] = _explore(full_path, depth + 1)
                else:
                    # If it's a file, try to read its contents
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            structure[item] = f.read()
                    except (UnicodeDecodeError, PermissionError):
                        # For binary or unreadable files, just store the path
                        structure[item] = "[Unreadable file]"
        
        except PermissionError:
            structure = "[Permission denied]"
        
        return structure

    return _explore(root_dir)

def print_structure(structure, indent=''):
    """
    Recursively print the directory structure with contents.
    
    :param structure: Dictionary representing directory structure
    :param indent: Indentation for hierarchical display
    """
    for key, value in structure.items():
        print(f"{indent}{key}")
        
        if isinstance(value, dict):
            # If value is a dictionary (subdirectory), recursively print
            print_structure(value, indent + '  ')
        elif value:
            # If value is a non-empty string (file contents)
            print(f"{indent}  Contents:")
            content_lines = value.split('\n')
            # Print first few lines of content
            for line in content_lines[:5]:
                print(f"{indent}    {line}")
            if len(content_lines) > 5:
                print(f"{indent}    ... (truncated)")

def main():
    # Check if directory path is provided
    if len(sys.argv) < 2:
        print("Please provide a directory path.")
        print("Usage: python directory_explorer.py /path/to/directory")
        sys.exit(1)
    
    # Get directory path from command line argument
    directory = sys.argv[1]
    
    # Validate directory
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        sys.exit(1)
    
    # Get absolute path
    directory = os.path.abspath(directory)
    
    print(f"Exploring directory: {directory}\n")
    print("Directory Structure and Contents:")
    print("-" * 40)
    
    # Get and print directory structure
    structure = get_dir_structure(directory)
    print_structure(structure)

if __name__ == "__main__":
    main()