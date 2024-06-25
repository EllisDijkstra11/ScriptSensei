from pprint import pprint
from kanji_class import Kanji, Stroke

input_kanji = None
template_kanji = None
size = []
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

def check_count():
    global input_kanji, template_kanji

    if input_kanji.get_strokes_length() == template_kanji.get_strokes_length():
        input_kanji.set_count(True)

    template_kanji.set_count(True)

def check_count_vectors(input_stroke: Stroke, template_stroke: Stroke):
    if input_stroke.get_stroke_length() == template_stroke.get_stroke_length():
        input_stroke.set_count(True)

    template_stroke.set_count(True)


# def compare_strokes():
#     global input, input_polar, template, template_polar, temp_input, temp_template

#     angle_matches = []
#     length_matches = []
#     length_differences = []
#     angle_differences = []

#     for stroke in range(len(input)):
#         if len(input[stroke]) == len(template[stroke]):
#             temp_input = input[stroke]
#             temp_template = template[stroke]
#             compare_vectors()
#         else:
#             delete_points()

#     print("Angle matches:\n", angle_matches, "\n", angle_differences, "\n\nLength matches:\n", length_matches, "\n", length_differences)
    
#     if not False in angle_matches and not False in length_matches:
#         return True
#     elif not False in angle_matches:
#         delete_points()
#     return False

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

