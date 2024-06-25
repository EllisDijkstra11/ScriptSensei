import numpy as np
from pprint import pprint
from kanji_class import Kanji, Stroke

input_kanji = None
template_kanji = None
wrong_kanji = None
size = []

length_scale = 0
length_tolerance = 5
angle_tolerance = 0.05

def compare_kanji(input_array, template_array):
    global input_kanji, template_kanji

    input_kanji = Kanji(input_array)
    template_kanji = Kanji(template_array)

    # Checks for the whole kanji
    check_count()
    
    # Checks for individual strokes
    current_strokes = 0
    if input_kanji == True or input_kanji.get_strokes_length() < template_kanji.get_strokes_length():
        current_strokes = input_kanji.get_strokes_length()
    else:
        current_strokes = template_kanji.get_strokes_length()
    
    for stroke in range(current_strokes):
        current_input_stroke = input_kanji.get_stroke(stroke)
        current_template_stroke = template_kanji.get_stroke(stroke)

        check_count_vectors(current_input_stroke, current_template_stroke)
        check_direction(current_input_stroke, current_template_stroke)
        if current_input_stroke.get_count:
            check_shape(current_input_stroke, current_template_stroke)
        else:
            delete_points(current_input_stroke, current_template_stroke)
    
    print("Count:", input_kanji.get_count())
    print("Count:", input_kanji.get_stroke(0).get_count())
    print("Direction:", input_kanji.get_stroke(0).get_direction())

def check_count():
    global input_kanji, template_kanji

    if input_kanji.get_strokes_length() == template_kanji.get_strokes_length():
        input_kanji.set_count(True)

    template_kanji.set_count(True)

def check_count_vectors(input_stroke: Stroke, template_stroke: Stroke):
    if input_stroke.get_stroke_length() == template_stroke.get_stroke_length():
        input_stroke.set_count(True)

    template_stroke.set_count(True)

def check_direction(input_stroke: Stroke, template_stroke: Stroke):
    angle_difference = abs(input_stroke.get_direction_vector()[0] - template_stroke.get_direction_vector()[0])
    input_length = input_stroke.get_direction_vector()[1]
    template_length = template_stroke.get_direction_vector()[1]

    if input_length * template_length * np.cos(angle_difference) > 0:
        input_stroke.set_direction(True)
    
    template_stroke.set_direction(True)

def check_shape(input_stroke: Stroke, template_stroke: Stroke):     
    angle_matches = []
    length_matches = []
    length_differences = []
    angle_differences = []

    # for stroke in range(len(input)):
    #     if len(input[stroke]) == len(template[stroke]):
    #         temp_input = input[stroke]
    #         temp_template = template[stroke]
    #         compare_vectors()
    #     else:
    #         delete_points()

    # print("Angle matches:\n", angle_matches, "\n", angle_differences, "\n\nLength matches:\n", length_matches, "\n", length_differences)
    
    # if not False in angle_matches and not False in length_matches:
    #     return True
    # elif not False in angle_matches:
    #     delete_points()
    # return False

def delete_points(input_stroke: Stroke, template_stroke: Stroke):
    input_vector = input_stroke.get_direction_vector()
    reverse_input_vector = input_stroke.get_reverse_direction_vector()
    template_vector = template_stroke.get_direction_vector()
    

# def compare_vectors(stroke):
#     global temp_input, temp_template, temp_input_polar, temp_template_polar

#     angle_matches = True
#     length_matches = True
#     length_differences = []
#     angle_differences = []

#     for vector in range(len(temp_input[stroke])):
#         angle_difference = abs(temp_input_polar[vector][0] - temp_template_polar[vector][0])
#         length_difference = abs(temp_input_polar[vector][1] - temp_template_polar[vector][1])

#         if angle_difference > angle_tolerance:
#             angle_matches = False

#         if length_difference > length_tolerance:
#             length_matches = False

#         angle_differences.append(angle_difference)
#         length_differences.append(length_difference)
    
#     if not False in angle_matches and not False in length_matches:
#         return True
    
#     # Check if the direction is wrong
#     elif not False in length_matches:
#         return change_direction()

#     return False


def change_direction():
    pass

def delete_points():
    pass

