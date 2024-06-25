import math
import numpy as np

class Stroke:
    def __init__(self, stroke, input):
        self.stroke = stroke
        self.reverse_stroke = self.stroke.reverse()
        self.vector_stroke = self.find_vector_stroke(self.stroke)
        self.reverse_vector_stroke = self.find_vector_stroke(self.reverse_stroke)
        self.polar_stroke = self.find_polar_stroke(self.stroke)
        self.reverse_polar_stroke = self.find_polar_stroke(self.reverse_stroke)

        # If it's an input character, assume being right; if it's a template character, set to True if checked
        self.direction = input
        self.order = input
        self.count = input

    def get_stroke(self):
        return self.stroke
    
    def get_reverse_stroke(self):
        return self.reverse_stroke

    def get_vector_stroke(self):
        return self.vector_stroke
    
    def get_reverse_vector_stroke(self):
        return self.reverse_vector_stroke

    def get_polar_stroke(self):
        return self.polar_stroke
    
    def get_reverse_polar_stroke(self):
        return self.reverse_polar_stroke

    def set_direction(self, direction):
        self.direction = direction

    def get_direction(self):
        return self.direction
            
    def set_order(self, order):
        self.order = order

    def get_order(self):
        return self.order
            
    def set_count(self, count):
        self.count = count

    def get_count(self):
        return self.count
    
    @staticmethod
    def find_vector_stroke(array):
        vectors = []

        for i in range(len(array) - 1):
            start = array[i]
            end = array[i + 1]
            vector = [end[0] - start[0], end[1] - start[1]]
            vectors.append(vector)
        
        return vectors

    @staticmethod
    def find_polar_stroke(array):
        polar_vectors = []

        for i in range(len(array) - 1):
            x, y = array[i]
            length = float(np.sqrt(x**2 + y**2))
            angle = float(np.arctan2(y, x))
            polar_vectors.append([angle, length])

        return polar_vectors

class Kanji:
    def __init__(self, strokes, input):
        # If it's an input character, assume being right; if it's a template character, set to True if checked
        self.input = input
        self.count = input
        self.strokes = []

        for stroke in strokes:
            self.add_stroke(stroke)

    def get_input(self):
        return self.input

    def add_stroke(self, stroke):
        stroke = Stroke(stroke, self.input)
        self.strokes.append(stroke)

    def get_stroke(self, index):
        if 0 <= index < len(self.strokes):
            return self.strokes[index]
        else:
            raise IndexError("Stroke index out of range")
    
    def get_strokes(self):
        return self.strokes
    
    def set_count(self, count):
        self.count = count
    
    def get_count(self):
        return self.count