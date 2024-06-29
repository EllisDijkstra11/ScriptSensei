import numpy as np
from pprint import pprint
from kanji_class import Kanji, Stroke
from itertools import combinations

input_kanji = None
template_kanji = None
wrong_kanji = None

scale = 0
size_tolerance = 5
angle_tolerance = 0.25

def compare_kanji(input_array, template_array):
    global input_kanji, template_kanji

    input_kanji = Kanji(input_array)
    template_kanji = Kanji(template_array)

    difference_number_of_strokes = check_count()
    # Checks for the whole kanji
    input_kanji.set_count(difference_number_of_strokes)
    
    matched_stroke_indexes = []
    for stroke_index in range(min(input_kanji.get_strokes_length(), template_kanji.get_strokes_length())):
        current_input_stroke: Stroke = input_kanji.get_stroke(stroke_index)
        current_template_stroke: Stroke = template_kanji.get_stroke(stroke_index)

        if check_direction(current_input_stroke, current_template_stroke):
            current_input_stroke.set_direction(True)
        else:
            current_input_stroke.reverse_strokes()

        compare_strokes(current_input_stroke, current_template_stroke)
        if not current_input_stroke.get_shape() == None:
            matched_stroke_indexes.append(stroke_index)
    
    for stroke_index in range(input_kanji.get_strokes_length()):
        if not stroke_index in matched_stroke_indexes:
            current_input_stroke: Stroke = input_kanji.get_stroke(stroke_index)
            current_input_stroke.set_false()
            best_index = None
            best_score = 0
            longest = 0

            for template_index in range(template_kanji.get_strokes_length()):
                current_template_stroke: Stroke = template_kanji.get_stroke(template_index)
                if current_template_stroke.get_shape() == None:
                    if check_direction(current_input_stroke, current_template_stroke):
                        current_input_stroke.set_direction(True)
                    else:
                        current_input_stroke.reverse_strokes()
                
                    compare_strokes(current_input_stroke, current_template_stroke)
                    if not current_input_stroke.get_shape() == None:
                        current_score = current_input_stroke.get_shape()
                        current_length = current_input_stroke.get_direction_vector()[1]
                        if current_score > best_score:
                            best_score = current_score
                            best_index = template_index
                            longest = current_length
                        elif current_score == best_score and current_length > longest:
                            best_score = current_score
                            best_index = template_index
                            longest = current_length

                current_input_stroke.set_false()
        
            if not best_index == None:
                current_template_stroke: Stroke = template_kanji.get_stroke(best_index)
                if check_direction(current_input_stroke, current_template_stroke):
                    current_input_stroke.set_direction(True)
                else:
                    current_input_stroke.reverse_strokes()
                compare_strokes(current_input_stroke, current_template_stroke)

    return find_score()

def compare_strokes(input_stroke: Stroke, template_stroke: Stroke):
    # If the directional vector between the starting and end point is similar
    if check_end_points(input_stroke, template_stroke):
        compare_vectors(input_stroke, template_stroke)

def compare_vectors(input_stroke: Stroke, template_stroke: Stroke):
        # If the strokes consist of an equal number of vectors
        if input_stroke.get_count():
            # If the shape is similar
            if check_shape(input_stroke, template_stroke):
                template_stroke.set_shape(True)
                input_stroke.set_shape(10)
                input_stroke.set_order(template_stroke.get_index() - input_stroke.get_index())    

                size = check_size(input_stroke, template_stroke)
                if not size == 0:
                    input_stroke.set_size(True)
                    input_kanji.add_size(size)
            else:
                delete_points(input_stroke, template_stroke)
        else:
            delete_points(input_stroke, template_stroke)

def check_count():
    global input_kanji, template_kanji

    input_kanji_length = input_kanji.get_strokes_length()
    template_kanji_length = template_kanji.get_strokes_length()

    difference = input_kanji_length - template_kanji_length

    return difference

def check_direction(input_stroke: Stroke, template_stroke: Stroke):
    angle_difference = abs(input_stroke.get_direction_vector()[0] - template_stroke.get_direction_vector()[0])
    if angle_difference > 2 * np.pi:
        angle_difference = angle_difference - 2 * np.pi
    
    if angle_difference < np.pi:
        return True
    return False

def check_shape(input_stroke: Stroke, template_stroke: Stroke):
    if input_stroke.get_stroke_length() != template_stroke.get_stroke_length():
        return False
    
    for point in range(input_stroke.get_stroke_length() - 1):
        input_vector = input_stroke.get_point(point)
        template_vector = template_stroke.get_point(point)
        angle_difference = abs(input_vector[0] - template_vector[0])
        if angle_difference > angle_tolerance:
            return False

    if check_size(input_stroke, template_stroke) == 0:
        return False
    return True

def check_size(input_stroke: Stroke, template_stroke: Stroke):
    global size_tolerance
    
    size = []
    for point in range(input_stroke.get_stroke_length() - 1):
        input_vector = input_stroke.get_point(point)
        template_vector = template_stroke.get_point(point)
        size.append(abs(input_vector[1] / template_vector[1]))
    
    if len(size) == 0:
        return 0
    
    average = sum(size) / len(size)  # Calculate average size
    
    if len(size) < 2:
        return average  # Single point or no size comparison needed

    for point in size:
        if abs(point - average) > size_tolerance:
            return 0
    
    return average

def check_end_points(input_stroke: Stroke, template_stroke: Stroke):
    global angle_tolerance

    input_vector = input_stroke.get_direction_vector()
    template_vector = template_stroke.get_direction_vector()

    angle_difference = abs(input_vector[0] - template_vector[0])
    if min(angle_difference, 2 * np.pi - angle_difference) < angle_tolerance:
        return True
    
    return False

def delete_points(input_stroke: Stroke, template_stroke: Stroke):
    global input_kanji

    input_stroke_stroke = input_stroke.get_stroke()
    template_stroke_stroke = template_stroke.get_stroke()
    temp_input_strokes = find_temp_stroke(input_stroke_stroke)
    temp_template_strokes = find_temp_stroke(template_stroke_stroke)

    longest_match = 0
    longest_temp_input = None
    longest_temp_template = None
    for temp_input_stroke in temp_input_strokes:
        temp_input = Stroke(temp_input_stroke)
        temp_input.set_index(input_stroke.get_index())
        for temp_template_stroke in temp_template_strokes:
            temp_template = Stroke(temp_template_stroke)
            temp_template.set_index(template_stroke.get_index())
            if check_shape(temp_input, temp_template):
                current_match = len(temp_input_stroke)
                if current_match > longest_match:
                    longest_match = current_match
                    longest_temp_input = temp_input
                    longest_temp_template = temp_template
    
    if longest_match != 0:
        template_stroke.set_shape(True)
        input_stroke.set_shape((longest_match / input_stroke.get_stroke_length()) * 10)
        input_stroke.set_order(template_stroke.get_index() - input_stroke.get_index())
            
        size = check_size(longest_temp_input, longest_temp_template)
        if not size == 0:
            input_stroke.set_size(True)
            input_kanji.add_size(size)

def find_temp_stroke(points):
    length = len(points)
    if length <= 2:
        return [points]

    subsets = [[points[0], points[-1]]]
    for r in range(length - 2, 0, -1):
        for subset in combinations(range(1, length - 1), r):
            subset_points = [points[0]] + [points[i] for i in subset] + [points[-1]]
            subsets.append(subset_points)
    return subsets

def find_score():
    global input_kanji, size_tolerance
    score = []
    print("\n\n\nChecking kanji")

    count = input_kanji.get_count()
    size = int(input_kanji.get_size(size_tolerance))
    direction = []
    order = []
    shape = []

    if count == 0:
        print("Number of strokes:    Correct")
    elif count < 0:
        print("Number of strokes:    Too few (" + str(count) + ")")
    else:
        print("Number of strokes:    Too many (" + str(count) + ")")
    print("Number of strokes:    Too many (" + str(count) + ")")
    print("Size:                 " + str(size) + "/10")
    

    for index in range(input_kanji.get_strokes_length()):
        stroke: Stroke = input_kanji.get_stroke(index)
        direction.append(stroke.get_direction())
        order.append(stroke.get_order())
        if not stroke.get_shape() == None:
            shape.append(int(stroke.get_shape()))
        else:
            shape.append(0)

        print("\nCurrent stroke:       " + str(index))
        print("   Stroke direction:     " + str(direction[-1]))
        print("   Shape order:          " + str(order[-1]))
        print("   Shape score:          " + str(shape[-1]) + "/10")
        if str(shape[-1]) == 0:
            print("   Stroke does not match")
        else:
            print("   Stroke matches!")
    
    score.append(count)
    score.append(size)
    score.append(direction)
    score.append(order)
    score.append(shape)
    
    return score
