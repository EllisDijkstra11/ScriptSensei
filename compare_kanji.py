import numpy as np
from pprint import pprint
from kanji_class import Kanji, Stroke
from itertools import combinations

input_kanji = None
template_kanji = None
wrong_kanji = None
size = []

scale = 0
length_tolerance = 50
angle_tolerance = 0.1

def compare_kanji(input_array, template_array):
    global input_kanji, template_kanji

    input_kanji = Kanji(input_array)
    template_kanji = Kanji(template_array)

    find_scale()
    scale_kanji()

    print("\n\n\nChecking kanji")


    difference_number_of_strokes = check_count()
    # Checks for the whole kanji
    if difference_number_of_strokes == 0:
        input_kanji.set_count(True)
    template_kanji.set_count(True)
    
    # Checks for individual strokes
    current_strokes = 0
    if difference_number_of_strokes == 0:
        current_strokes = input_kanji.get_strokes_length()
    elif difference_number_of_strokes < 0:
        current_strokes = input_kanji.get_strokes_length()
    else:
        current_strokes = template_kanji.get_strokes_length()
    
    for stroke in range(current_strokes):
        print("\nCurrent stroke:       " + str(stroke))
        current_input_stroke: Stroke = input_kanji.get_stroke(stroke)
        current_template_stroke: Stroke = template_kanji.get_stroke(stroke)

        if check_count_vectors(current_input_stroke, current_template_stroke):
            current_input_stroke.set_count(True)
        current_template_stroke.set_count(True)

        if check_direction(current_input_stroke, current_template_stroke):
            current_input_stroke.set_direction(True)
        else:
            current_input_stroke = Stroke(input_kanji.get_reverse_stroke(stroke))
        current_template_stroke.set_direction(True)

        # If the directional vector between the starting and end point is similar
        if check_end_points(current_input_stroke, current_template_stroke):
            compare_vectors(current_input_stroke, current_template_stroke)
        else:
            print("   Stroke does not match")

def compare_vectors(input_stroke: Stroke, template_stroke: Stroke):
        # If the strokes consist of an equal number of vectors
        if input_stroke.get_count():
            # If the shape is similar
            if check_shape(input_stroke, template_stroke):
                input_stroke.set_shape(True)
                input_stroke.set_shape_score(10)
                print("   Shape score:          10/10")
                print("   Stroke matches!")
            else:
                delete_points(input_stroke, template_stroke)
        else:
            delete_points(input_stroke, template_stroke)

def find_scale():
    global input_kanji, template_kanji, scale

    input_x, input_y = find_min_max(input_kanji)
    template_x, template_y = find_min_max(template_kanji)
    
    scale_x = template_x / input_x
    scale_y = template_y / input_y

    scale = max(scale_x, scale_y)

def find_min_max(kanji):
    all_points = [point for stroke in kanji.get_strokes() for point in stroke.get_stroke()]
    all_x = [point[0] for point in all_points]
    all_y = [point[1] for point in all_points]

    min_x = min(all_x)
    max_x = max(all_x)
    min_y = min(all_y)
    max_y = max(all_y)

    return max_x - min_x, max_y - min_y

def scale_kanji():
    global input_kanji, scale

    for stroke in input_kanji.get_strokes():
        scaled_stroke = [[point[0] * scale, point[1] * scale] for point in stroke.get_stroke()]
        stroke.set_stroke(scaled_stroke)

def check_count():
    global input_kanji, template_kanji

    input_kanji_length = input_kanji.get_strokes_length()
    template_kanji_length = template_kanji.get_strokes_length()

    difference = input_kanji_length - template_kanji_length

    if difference == 0:
        print("Number of strokes:    Correct")
    elif difference < 0:
        print("Number of strokes:    Too few (" + str(-difference) + ")")
    else:
        print("Number of strokes:    Too many (" + str(difference) + ")")

    return difference

def check_count_vectors(input_stroke: Stroke, template_stroke: Stroke):
    if input_stroke.get_stroke_length() == template_stroke.get_stroke_length():
        return True

    return False

def check_direction(input_stroke: Stroke, template_stroke: Stroke):
    angle_difference = abs(input_stroke.get_direction_vector()[0] - template_stroke.get_direction_vector()[0])
    input_length = input_stroke.get_direction_vector()[1]
    template_length = template_stroke.get_direction_vector()[1]

    if input_length * template_length * np.cos(angle_difference) > 0:
        print("   Stroke direction:     Correct")
        return True

    print("   Stroke direction:     Wrong")
    return False

def check_shape(input_stroke: Stroke, template_stroke: Stroke):
    if input_stroke.get_stroke_length() != template_stroke.get_stroke_length():
        return False
    
    for point in range(input_stroke.get_stroke_length()):
        input_vector = input_stroke.get_point(point)
        template_vector = template_stroke.get_point(point)
        angle_difference = abs(input_vector[0] - template_vector[0])
        if min(angle_difference, 2 * np.pi - angle_difference) > angle_tolerance or abs(input_vector[1] - template_vector[1]) > length_tolerance:
            return False
    
    return True        

def check_end_points(input_stroke: Stroke, template_stroke: Stroke):
    global angle_tolerance, length_tolerance

    input_vector = None
    if input_stroke.get_direction():
        input_vector = input_stroke.get_direction_vector()
    else:
        input_vector = input_stroke.get_reverse_direction_vector()

    template_vector = template_stroke.get_direction_vector()

    angle_difference = abs(input_vector[0] - template_vector[0])
    if min(angle_difference, 2 * np.pi - angle_difference) < angle_tolerance and abs(input_vector[1] - template_vector[1]) < length_tolerance:
        return True
    
    return False

def delete_points(input_stroke: Stroke, template_stroke: Stroke):
    global angle_tolerance, length_tolerance

    input_vectors = input_stroke.get_vector_stroke()
    template_vectors = template_stroke.get_vector_stroke()
    temp_input_vectors = find_temp_vectors(input_vectors)
    temp_template_vectors = find_temp_vectors(template_vectors)

    longest_match = 0
    for input_vector in temp_input_vectors:
        for template_vector in temp_template_vectors:
            temp_input = Stroke(input_vector)
            temp_template = Stroke(template_vector)
            if check_shape(temp_input, temp_template):
                current_match = len(input_vector)
                if current_match > longest_match:
                    longest_match = longest_match
    
    if longest_match != 0:
        input_stroke.set_shape(True)
        input_stroke.set_shape_score((longest_match / input_stroke.get_stroke_length()) * 10)
        print("   Shape score:          " + str(int(input_stroke.get_shape_score())) + "/10")
        print("   Stroke matches!")
     

def find_best_matching_strokes(input_stroke: Stroke, template_stroke: Stroke):
    input_points = [input_stroke.get_point(i) for i in range(input_stroke.get_stroke_length())]
    template_points = [template_stroke.get_point(i) for i in range(template_stroke.get_stroke_length())]

    input_subsets = find_temp_vectors(input_points)
    template_subsets = find_temp_vectors(template_points)

    best_match = (input_stroke, template_stroke)
    max_points_kept = 0

    for input_subset in input_subsets:
        for template_subset in template_subsets:
            input_subset_stroke = Stroke(input_subset)
            template_subset_stroke = Stroke(template_subset)
            if check_shape(input_subset_stroke, template_subset_stroke):
                points_kept = len(input_subset)
                if points_kept > max_points_kept:
                    best_match = (input_subset_stroke, template_subset_stroke)
                    max_points_kept = points_kept

    return best_match

def find_temp_vectors(points):
    length = len(points)
    if length <= 2:
        return [points]

    subsets = []
    for r in range(length - 2, 0, -1):
        for subset in combinations(range(1, length - 1), r):
            subset_points = [points[0]] + [points[i] for i in subset] + [points[-1]]
            subsets.append(subset_points)
    return subsets
