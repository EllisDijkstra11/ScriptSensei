import numpy as np
from pprint import pprint
from kanji_class import Kanji, Stroke
from itertools import combinations

input_kanji = None
template_kanji = None
wrong_kanji = None

scale = 0
size_tolerance = 0.1
angle_tolerance = 0.1

def compare_kanji(input_array, template_array):
    print("I'm here now")
    global input_kanji, template_kanji

    input_kanji = Kanji(input_array)
    template_kanji = Kanji(template_array)

    print("\n\n\nChecking kanji")

    difference_number_of_strokes = check_count()
    # Checks for the whole kanji
    if difference_number_of_strokes == 0:
        input_kanji.set_count(True)
    template_kanji.set_count(True)
    
    matched_stroke_indexes = []
    for stroke_index in range(min(input_kanji.get_strokes_length(), template_kanji.get_strokes_length())):
        print("\nCurrent stroke:       " + str(stroke_index))
        current_input_stroke: Stroke = input_kanji.get_stroke(stroke_index)
        current_template_stroke: Stroke = template_kanji.get_stroke(stroke_index)

        if check_direction(current_input_stroke, current_template_stroke):
            current_input_stroke.set_direction(True)
        else:
            current_input_stroke.reverse_strokes()

        compare_strokes(current_input_stroke, current_template_stroke)
        if current_input_stroke.get_shape():
            matched_stroke_indexes.append(stroke_index)
    
    for stroke_index in range(input_kanji.get_strokes_length()):
        if not stroke_index in matched_stroke_indexes:
            current_input_stroke: Stroke = input_kanji.get_stroke(stroke_index)
            current_input_stroke.set_false()
            best_index = None
            best_score = 0

            for template_index in range(template_kanji.get_strokes_length()):
                current_template_stroke: Stroke = template_kanji.get_stroke(template_index)
                if not current_template_stroke.get_shape():
                    if check_direction(current_input_stroke, current_template_stroke):
                        current_input_stroke.set_direction(True)
                    else:
                        current_input_stroke.reverse_strokes()
                
                    compare_strokes(current_input_stroke, current_template_stroke)
                    if current_input_stroke.get_shape():
                        current_score = current_input_stroke.get_shape_score()
                        if current_score > best_score:
                            best_score = current_score
                            best_index = template_index

                current_input_stroke.set_false()
        
            if not best_index == None:
                current_template_stroke: Stroke = template_kanji.get_stroke(best_index)
                compare_strokes(current_input_stroke, current_template_stroke)


    return find_score()

def compare_strokes(input_stroke: Stroke, template_stroke: Stroke):
    if check_count_vectors(input_stroke, template_stroke):
        input_stroke.set_count(True)

    # If the directional vector between the starting and end point is similar
    if check_end_points(input_stroke, template_stroke):
        compare_vectors(input_stroke, template_stroke)
    else:
        print("   Stroke does not match")

def compare_vectors(input_stroke: Stroke, template_stroke: Stroke):
        # If the strokes consist of an equal number of vectors
        if input_stroke.get_count():
            # If the shape is similar
            if check_shape(input_stroke, template_stroke):
                input_stroke.set_shape(True)
                template_stroke.set_shape(True)
                input_stroke.set_shape_score(10)
                input_stroke.set_order(template_stroke.get_index() - input_stroke.get_index())    

                if check_size(input_stroke, template_stroke):
                    input_stroke.set_size(True)

                print("   Shape score:          10/10")
                print("   Stroke matches!")
            else:
                delete_points(input_stroke, template_stroke)
        else:
            delete_points(input_stroke, template_stroke)

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
    
    for point in range(input_stroke.get_stroke_length() - 1):
        input_vector = input_stroke.get_point(point)
        template_vector = template_stroke.get_point(point)
        angle_difference = abs(input_vector[0] - template_vector[0])
        if min(angle_difference, 2 * np.pi - angle_difference) > angle_tolerance:
            return False

    return True

def check_size(input_stroke: Stroke, template_stroke: Stroke):
    global input_kanji

    if input_stroke.get_stroke_length() != template_stroke.get_stroke_length():
        return False
    
    global size_tolerance
    size = []
    for point in range(input_stroke.get_stroke_length() - 1):
        input_vector = input_stroke.get_point(point)
        template_vector = template_stroke.get_point(point)
        size.append(abs(input_vector[1] / template_vector[1]))
    
    if len(size) < 2:
        return True  # Single point or no size comparison needed
    
    average = sum(size) / len(size)  # Calculate average size
    input_kanji.add_size(average)

    for point in size:
        if abs(point - average) > size_tolerance:
            return False
    
    return True

def check_end_points(input_stroke: Stroke, template_stroke: Stroke):
    global angle_tolerance

    input_vector = input_stroke.get_direction_vector()
    template_vector = template_stroke.get_direction_vector()

    angle_difference = abs(input_vector[0] - template_vector[0])
    if min(angle_difference, 2 * np.pi - angle_difference) < angle_tolerance:
        return True
    
    return False

def delete_points(input_stroke: Stroke, template_stroke: Stroke):
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
        template_stroke.set_shape(True)
        input_stroke.set_shape_score((longest_match / input_stroke.get_stroke_length()) * 10)
        input_stroke.set_order(template_stroke.get_index() - input_stroke.get_index())
            
        if check_size(input_stroke, template_stroke):
            input_stroke.set_size(True)

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

def find_score():
    global size_tolerance
    score = []

    count = input_kanji.get_count()
    size = input_kanji.get_size(size_tolerance)
    direction = []
    order = []
    shape = []

    for index in range(input_kanji.get_strokes_length()):
        stroke: Stroke = input_kanji.get_stroke(index)
        direction.append(stroke.get_direction())
        order.append(stroke.get_order())
        shape.append(stroke.get_shape_score())
    
    score.append(count)
    score.append(size)
    score.append(direction)
    score.append(order)
    score.append(shape)
    return score
