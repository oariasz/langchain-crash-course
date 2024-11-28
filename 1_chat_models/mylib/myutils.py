import os

def clear_screen():
    os.system('clear')
    """
    Clears the terminal screen on macOS and Windows.
    """
    # Check the operating system and execute the corresponding command
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For macOS and other Unix-like systems
        os.system('clear')