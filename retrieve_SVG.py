from svgpathtools import parse_path
import xml.etree.ElementTree as ET

def extractSVGPaths(svg_path):
    try:
        tree = ET.parse(svg_path)  # Parse SVG file directly from path
        root = tree.getroot()
        paths = []
        for elem in root.iter():
            if elem.tag.endswith('path'):
                paths.append(elem.attrib['d'])
        return paths
    except Exception as e:
        print(f"Error parsing SVG file {svg_path}: {e}")
        return []
    
def svgPathToPoints(path_data):
    path = parse_path(path_data)
    points = []
    
    for segment in path:
        if segment.start is not None:
            points.append([segment.start.real, segment.start.imag])
        
        if segment.end is not None:
            points.append([segment.end.real, segment.end.imag])
    
    return points