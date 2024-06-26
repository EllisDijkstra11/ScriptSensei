import math
import numpy as np

class Stroke:
    def __init__(self, stroke):
        self.set_stroke(stroke)

        self.order = None
        self.direction = False
        self.count = False
        self.size = False
        self.shape = False
        self.shape_score = 0
        self.index = None
        self.reversed_strokes = False
    
    def set_stroke(self, stroke):
        self.stroke = stroke
        self.reverse_stroke = self.find_reverse_stroke(self.stroke)
        self.vector_stroke = self.find_vector_stroke(self.stroke)
        self.polar_stroke = self.find_polar_stroke(self.vector_stroke)
        self.direction_vector = self.find_direction_vector(self.stroke[0], self.stroke[-1])
        self.reverse_direction_vector = self.find_direction_vector(self.reverse_stroke[0], self.reverse_stroke[-1])

    def get_stroke(self):
        return self.stroke
    
    def get_point(self, index):
        return self.polar_stroke[index]
    
    def get_reverse_stroke(self):
        return self.reverse_stroke

    def get_vector_stroke(self):
        return self.vector_stroke

    def get_polar_stroke(self):
        return self.polar_stroke
    
    def get_direction_vector(self):
        return self.direction_vector

    def get_reverse_direction_vector(self):
        return self.reverse_direction_vector
    
    def get_stroke_length(self):
        return len(self.stroke)

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
    
    def set_size(self, size):
        self.size = size
    
    def get_size(self):
        return self.size
            
    def set_shape(self, shape):
        self.shape = shape

    def get_shape(self):
        return self.shape
            
    def set_shape_score(self, shape_score):
        self.shape_score = shape_score

    def get_shape_score(self):
        return self.shape_score
            
    def set_index(self, index):
        self.index = index

    def get_index(self):
        return self.index
    
    def reverse_strokes(self):
        self.reversed_strokes = True
        self.reverse_stroke = self.stroke
        self.stroke = self.find_reverse_stroke(self.stroke)
        self.vector_stroke = self.find_vector_stroke(self.stroke)
        self.polar_stroke = self.find_polar_stroke(self.vector_stroke)
        self.direction_vector = self.find_direction_vector(self.stroke[0], self.stroke[-1])
        self.reverse_direction_vector = self.find_direction_vector(self.reverse_stroke[0], self.reverse_stroke[-1])
    
    def set_false(self):
        if self.reversed_strokes:
            self.reverse_strokes()

        self.order = None
        self.direction = False
        self.count = False
        self.size = False
        self.shape = False
        self.shape_score = 0
        self.index = None
        self.reversed_strokes = False

    @staticmethod
    def find_reverse_stroke(stroke):
        reverse_stroke = []
        for point in stroke:
            reverse_stroke.insert(0, point)
        return reverse_stroke
    
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
    def find_polar_stroke(vectors):
        polar_vectors = []

        for i in range(len(vectors)):
            x, y = vectors[i]
            length = float(np.sqrt(x**2 + y**2))
            angle = float(np.arctan2(y, x))
            polar_vectors.append([angle, length])

        return polar_vectors

    @staticmethod
    def find_direction_vector(start, end):
        vector = [end[0] - start[0], end[1] - start[1]]
        x, y = vector
        length = float(np.sqrt(x**2 + y**2))
        angle = float(np.arctan2(y, x))
        return [angle, length]

class Kanji:
    def __init__(self, strokes):
        self.input = False
        self.count = False
        self.strokes = []
        self.size = []

        for index in range(len(strokes)):
            vectors = strokes[index]
            self.add_stroke(vectors)
            self.get_stroke(index).set_index(index)

    def get_input(self):
        return self.input

    def add_stroke(self, vectors):
        stroke = Stroke(vectors)
        self.strokes.append(stroke)

    def get_stroke(self, index):
        if 0 <= index < len(self.strokes):
            return self.strokes[index]
        else:
            raise IndexError("Stroke index out of range")

    def get_reverse_stroke(self, index):
        if 0 <= index < len(self.strokes):
            return self.strokes[index].get_reverse_stroke()
        else:
            raise IndexError("Stroke index out of range")
    
    def get_strokes(self):
        return self.strokes
    
    def get_strokes_length(self):
        return len(self.strokes)
    
    def set_count(self, count):
        self.count = count
    
    def get_count(self):
        return self.count
    
    def add_size(self, size):
        self.size.append[size]
    
    def get_size(self, size_tolerance):
        count = 0
        average = sum(self.size) / len(self.size)  # Calculate average size

        for point in self.size:
            if abs(point - average) < size_tolerance:
                count += 1
    
        return count / len(self.size)
