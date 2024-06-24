import os

def listSvgFiles(directory):
    """
    Lists all SVG files in the given directory.
    
    Args:
        directory (str): The directory path to search for SVG files.
    
    Returns:
        list: A list of file paths for all SVG files in the directory.
    """
    svg_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.svg'):
                svg_files.append(os.path.join(root, file))
    return svg_files