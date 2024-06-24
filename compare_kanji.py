import numpy as np
import math
from pprint import pprint

input = []
template = []
input_polar = []
template_polar = []
temp_input = []
temp_template = []
temp_input_polar = []
temp_template_polar = []
size = []
length_tolerance = 5
angle_tolerance = 0.05

def compare_kanji(input_array, template_array):
    global input, input_polar, template, template_polar
    input, input_polar = array_to_vector(input_array)
    template, template_polar = array_to_vector(template_array)

    if len(input) == len(template):
        boolean = compare_vectors()
        print("Boolean", boolean)

    print('input:', input_array, "\nvector:", input, '\ntemplate:', template_array, "\nvector:", template)

def array_to_vector(arrays):
    vector_arrays = []
    polar_arrays = []

    for array in arrays:
        vectors = []
        polar_vectors = []

        for i in range(len(array) - 1):
            start = array[i]
            end = array[i + 1]
            vector = [end[0] - start[0], end[1] - start[1]]
            vectors.append(vector)

            angle, length = vector_to_polar(vector)
            polar_vectors.append([angle, length])
        vector_arrays.append(vectors)
        polar_arrays.append(polar_vectors)

    # Process each array of coordinates
    return vector_arrays, polar_arrays

def vector_to_polar(vector):
    x, y = vector
    length = float(np.sqrt(x**2 + y**2))
    angle = float(np.arctan2(y, x))
    return angle, length

def normalize_vectors(vector):
    length = math.sqrt(vector[0]**2 + vector[1]**2)
    if length == 0:  # Avoid division by zero
        return vector
    return [vector[0] / length, vector[1] / length]

def compare_strokes():
    global input, input_polar, template, template_polar, temp_input, temp_template

    angle_matches = []
    length_matches = []
    length_differences = []
    angle_differences = []

    for stroke in range(len(input)):
        if len(input[stroke]) == len(template[stroke]):
            temp_input = input[stroke]
            temp_template = template[stroke]
            compare_vectors()
        else:
            delete_points()

    print("Angle matches:\n", angle_matches, "\n", angle_differences, "\n\nLength matches:\n", length_matches, "\n", length_differences)
    
    if not False in angle_matches and not False in length_matches:
        return True
    elif not False in angle_matches:
        delete_points()
    return False

def compare_vectors(stroke):
    global temp_input, temp_template, temp_input_polar, temp_template_polar

    angle_matches = True
    length_matches = True
    length_differences = []
    angle_differences = []

    for vector in range(len(temp_input[stroke])):
        angle_difference = abs(temp_input_polar[vector][0] - temp_template_polar[vector][0])
        length_difference = abs(temp_input_polar[vector][1] - temp_template_polar[vector][1])

        if angle_difference > angle_tolerance:
            angle_matches = False

        if length_difference > length_tolerance:
            length_matches = False

        angle_differences.append(angle_difference)
        length_differences.append(length_difference)
    
    if not False in angle_matches and not False in length_matches:
        return True
    
    # Check if the direction is wrong
    elif not False in length_matches:
        return change_direction(compare_vectors)

    return False


def change_direction():


def delete_points():
    pass

