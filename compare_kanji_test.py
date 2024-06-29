import unittest
import numpy as np
from kanji_class import Stroke, Kanji
import compare_kanji as kanji

# Sample data for testing
correct_data = [
    [[0, 0], [1, 1]],  # First stroke of input kanji
    [[2, 2], [3, 3]]   # Second stroke of input kanji
]

wrong_direction_data = [
    [[0, 0], [1, 1]],  # First stroke of input kanji
    [[3, 3], [2, 2]]   # Second stroke of input kanji in wrong direction
]

wrong_order_data = [
    [[2, 2], [3, 3]],  # First stroke of input kanji
    [[0, 0], [1, 1]]   # Second stroke of input kanji in wrong order
]

wrong_shape_data = [
    [[0, 0], [1, 1]],      # First stroke of input kanji
    [[2, 3], [3, 6]]       # Second stroke of input kanji with different shape
]

too_few_strokes_data = [
    [[0, 0], [1, 1]]   # Only one stroke instead of two
]

too_many_strokes_data = [
    [[0, 0], [1, 1]],  # First stroke of input kanji
    [[2, 2], [3, 3]],  # Second stroke of input kanji
    [[4, 4], [5, 5]]   # Extra third stroke
]

too_few_strokes_data_wrong_order = [
    [[3, 3], [2, 2]]   # Only one stroke instead of two
]

too_many_strokes_data_wrong_order = [
    [[4, 4], [5, 5]],   # Extra third stroke
    [[0, 0], [1, 1]],  # First stroke of input kanji
    [[2, 2], [3, 3]]  # Second stroke of input kanji
]

different_scaling_data = [
    [[0, 0], [2, 2]],     # First stroke scaled differently
    [[4, 4], [6, 6]]      # Second stroke scaled differently
]

uniform_scaling_data = [
    [[0, 0], [2, 2]],     # First stroke uniformly scaled
    [[4, 4], [8, 8]]      # Second stroke uniformly scaled
]

too_many_points_data = [
    [[0, 0], [4, 4], [5, 5], [1, 1]],  # First stroke of input kanji
    [[2, 2], [3, 3]]  # Second stroke of input kanji
]

template_data = [
    [[0, 0], [1, 1]],  # First stroke of template kanji
    [[2, 2], [3, 3]]   # Second stroke of template kanji
]

wrong_data = [
    [[8, 3], [2, 3], [4, 1]],
    [[3, 2], [1, 6], [5, 7]],
    [[5, 6], [10, 2]]
]

class TestStrokeTypes(unittest.TestCase):
    
    def setUp(self):
        self.stroke_data = [[0, 0], [3, 4]]
        self.stroke = Stroke(self.stroke_data)

    def test_set_stroke(self):
        self.assertEqual(self.stroke.get_stroke(), self.stroke_data)
        self.assertEqual(self.stroke.get_stroke_length(), 2)
        self.assertEqual(self.stroke.get_reverse_stroke(), [[3, 4], [0, 0]])  # Reverse stroke should be set to None initially
    
    def test_reverse_stroke_initialization(self):
        # Test case 1: Regular stroke initialization
        stroke_data = [[0, 0], [1, 1]]
        stroke = Stroke(stroke_data)
        
        self.assertEqual(stroke.get_stroke(), stroke_data)
        self.assertEqual(stroke.get_reverse_stroke(), [[1, 1], [0, 0]])

        # Test case 3: Single point stroke initialization
        single_point_data = [[2, 2]]
        single_point_stroke = Stroke(single_point_data)

        self.assertEqual(single_point_stroke.get_stroke(), single_point_data)
        self.assertEqual(single_point_stroke.get_reverse_stroke(), [[2, 2]])

    def test_find_vector_stroke(self):
        vectors = self.stroke.get_vector_stroke()
        expected_vectors = [[3, 4]]
        self.assertEqual(vectors, expected_vectors)

    def test_find_polar_stroke(self):
        polar_vectors = self.stroke.get_polar_stroke()
        length = float(np.sqrt(3**2 + 4**2))
        angle = float(np.arctan2(4, 3))
        expected_polar_vectors = [[angle, length]]
        self.assertEqual(polar_vectors, expected_polar_vectors)

    def test_stroke_attributes(self):
        self.stroke.set_direction(True)
        self.stroke.set_order(True)
        self.stroke.set_count(True)
        self.stroke.set_shape(True)
        
        self.assertTrue(self.stroke.get_direction())
        self.assertTrue(self.stroke.get_order())
        self.assertTrue(self.stroke.get_count())
        self.assertTrue(self.stroke.get_shape())

class TestKanjiComparison(unittest.TestCase):
    
    def setUp(self):
        global correct_data, template_data

        kanji.input_kanji = Kanji(correct_data)
        kanji.template_kanji = Kanji(template_data)

    def test_compare_kanji(self):
        global correct_data, template_data, wrong_data

        kanji.compare_kanji(correct_data, template_data)
        self.assertEqual(0, kanji.input_kanji.get_count())
        self.assertEqual(0, kanji.template_kanji.get_count())
        
        kanji.compare_kanji(correct_data, wrong_data)
        self.assertEqual(-1, kanji.input_kanji.get_count())
        self.assertEqual(0, kanji.template_kanji.get_count())

    def test_check_count(self):
        self.assertEqual(kanji.check_count(), 0)

        global correct_data, wrong_data
        kanji.input_kanji = Kanji(correct_data)
        kanji.template_kanji = Kanji(wrong_data)
        
        self.assertLess(kanji.check_count(), 0)

    def test_check_count_vectors(self):
        input_stroke = kanji.input_kanji.get_stroke(0)
        template_stroke = kanji.template_kanji.get_stroke(0)

        # self.assertTrue(kanji.check_count_vectors(input_stroke, template_stroke))

        global correct_data, wrong_data
        kanji.input_kanji = Kanji(correct_data)
        kanji.template_kanji = Kanji(wrong_data)

        input_stroke = kanji.input_kanji.get_stroke(0)
        template_stroke = kanji.template_kanji.get_stroke(0)

        # self.assertFalse(kanji.check_count_vectors(input_stroke, template_stroke))

    def test_check_direction(self):
        input_stroke = kanji.input_kanji.get_stroke(0)
        template_stroke = kanji.template_kanji.get_stroke(0)

        self.assertTrue(kanji.check_direction(input_stroke, template_stroke))

        global correct_data, wrong_data
        kanji.input_kanji = Kanji(correct_data)
        kanji.template_kanji = Kanji(wrong_data)

        input_stroke = kanji.input_kanji.get_stroke(0)
        template_stroke = kanji.template_kanji.get_stroke(0)

        self.assertFalse(kanji.check_direction(input_stroke, template_stroke))

    def test_stroke_variables(self):
        stroke = Stroke([[0, 0], [1, 1]])
        stroke.set_direction(True)
        stroke.set_order(True)
        stroke.set_count(True)
        stroke.set_shape(True)
        
        self.assertTrue(stroke.get_direction())
        self.assertTrue(stroke.get_order())
        self.assertTrue(stroke.get_count())
        self.assertTrue(stroke.get_shape())
    
    def test_kanji_variables(self):
        self.assertEqual(len(kanji.input_kanji.get_strokes()), 2)
        self.assertEqual(kanji.input_kanji.get_strokes_length(), 2)

class TestCheckShape(unittest.TestCase):

    def test_check_shape_true(self):
        input_stroke = Stroke([[0, 1], [np.pi/4, 2], [np.pi/2, 3]])
        template_stroke = Stroke([[0, 1], [np.pi/4, 2], [np.pi/2, 3]])
        
        self.assertTrue(kanji.check_shape(input_stroke, template_stroke))

    def test_check_shape_false_due_to_angle(self):
        input_stroke = Stroke([[0, 1], [np.pi/4, 2], [np.pi/2, 3]])
        template_stroke = Stroke([[0, 1], [np.pi/2, 2], [np.pi/2, 3]])
        
        self.assertFalse(kanji.check_shape(input_stroke, template_stroke))

    def test_check_shape_edge_case_angle_tolerance(self):
        input_stroke = Stroke([[0, 1], [np.pi/4, 2], [np.pi/2, 3]])
        template_stroke = Stroke([[0, 1], [np.pi/4 + kanji.angle_tolerance/2, 2], [np.pi/2, 3]])
        
        self.assertTrue(kanji.check_shape(input_stroke, template_stroke))

class TestStrokeMistakes(unittest.TestCase):
    
    def setUp(self):
        self.kanji_template = Kanji(correct_data)

    def compare_and_assert(self, input_data, template_data, expected_output):
        kanji.compare_kanji(input_data, template_data)
        
        self.assertEqual(kanji.input_kanji.get_count(), expected_output['count'])

        for i, expected_stroke in enumerate(expected_output['strokes']):
            input_stroke = kanji.input_kanji.get_stroke(i)

            self.assertEqual(input_stroke.get_direction(), expected_stroke['direction'])
            # self.assertEqual(input_stroke.get_shape(), expected_stroke['shape'])
            # self.assertEqual(input_stroke.get_count(), expected_stroke['count'])
            self.assertEqual(input_stroke.get_size(), expected_stroke['size'])

            # Check if the print statements match the expected output
            if not input_stroke.get_shape() == None:
                self.assertEqual(int(input_stroke.get_shape()), expected_stroke.get('shape_score', 0))
            else:
                self.assertEqual(input_stroke.get_shape(), expected_stroke.get('shape_score', 0))

    def test_correct_kanji(self):
        expected_output = {
            'count': 0,
            'strokes': [
                {'direction': True, 'shape': True, 'count': True, 'shape_score': 10, 'size': True},
                {'direction': True, 'shape': True, 'count': True, 'shape_score': 10, 'size': True}
            ]
        }
        self.compare_and_assert(correct_data, correct_data, expected_output)

    def test_wrong_direction(self):
        expected_output = {
            'count': 0,
            'strokes': [
                {'direction': True, 'shape': True, 'count': True, 'shape_score': 10, 'size': True},
                {'direction': False, 'shape': True, 'count': True, 'shape_score': 10, 'size': True}
            ]
        }
        self.compare_and_assert(wrong_direction_data, correct_data, expected_output)

    def test_wrong_order(self):
        expected_output = {
            'count': 0,
            'strokes': [
                {'direction': True, 'shape': True, 'count': True, 'shape_score': 10, 'size': True},
                {'direction': True, 'shape': True, 'count': True, 'shape_score': 10, 'size': True}
            ]
        }
        self.compare_and_assert(wrong_order_data, correct_data, expected_output)

    def test_wrong_shape(self):
        expected_output = {
            'count': 0,
            'strokes': [
                {'direction': True, 'shape': True, 'count': True, 'shape_score': 10, 'size': True},
                {'direction': False, 'shape': False, 'count': True, 'shape_score': None, 'size': False}
            ]
        }
        self.compare_and_assert(wrong_shape_data, correct_data, expected_output)

    def test_too_few_strokes(self):
        expected_output = {
            'count': -1,
            'strokes': [
                {'direction': True, 'shape': True, 'count': True, 'shape_score': 10, 'size': True},
            ]
        }
        self.compare_and_assert(too_few_strokes_data, correct_data, expected_output)

    def test_too_many_strokes(self):
        expected_output = {
            'count': 1,
            'strokes': [
                {'direction': True, 'shape': True, 'count': True, 'shape_score': 10, 'size': True},
                {'direction': True, 'shape': True, 'count': True, 'shape_score': 10, 'size': True},
                {'direction': False, 'shape': False, 'count': False, 'shape_score': None, 'size': False}
            ]
        }
        self.compare_and_assert(too_many_strokes_data, correct_data, expected_output)

    def test_too_few_strokes_wrong_order(self):
        expected_output = {
            'count': -1,
            'strokes': [
                {'direction': False, 'shape': True, 'count': True, 'shape_score': 10, 'size': True},
            ]
        }
        self.compare_and_assert(too_few_strokes_data_wrong_order, correct_data, expected_output)

    def test_too_many_strokes_wrong_order(self):
        expected_output = {
            'count': 1,
            'strokes': [
                {'direction': True, 'shape': True, 'count': True, 'shape_score': 10, 'size': True},
                {'direction': True, 'shape': True, 'count': True, 'shape_score': 10, 'size': True},
                {'direction': False, 'shape': False, 'count': False, 'shape_score': None, 'size': False}
            ]
        }
        self.compare_and_assert(too_many_strokes_data_wrong_order, correct_data, expected_output)

    def test_different_scaling_factor(self):
        correct_data = [
            [[0, 0], [1, 1], [4, 4]],  # First stroke of input kanji
            [[2, 2], [3, 3], [4, 4]]   # Second stroke of input kanji
        ]

        different_scaling_data = [
            [[0, 0], [2, 2], [8, 8]],     # First stroke scaled differently
            [[4, 4], [6, 6], [10, 10]]      # Second stroke scaled differently
        ]
        expected_output = {
            'count': 0,
            'strokes': [
                {'direction': True, 'shape': True, 'count': True, 'shape_score': 10, 'size': True},  # Direction should match, shape should not
                {'direction': True, 'shape': True, 'count': True, 'shape_score': 10, 'size': True}   # Direction should match, shape should not
            ]
        }
        self.compare_and_assert(different_scaling_data, correct_data, expected_output)

    def test_uniform_scaling_factor(self):
        expected_output = {
            'count': 0,
            'strokes': [
                {'direction': True, 'shape': True, 'count': True, 'shape_score': 10, 'size': True},
                {'direction': True, 'shape': True, 'count': True, 'shape_score': 10, 'size': True}
            ]
        }
        self.compare_and_assert(uniform_scaling_data, correct_data, expected_output)
    
    def test_too_many_points_input(self):
        expected_output = {
            'count': 0,
            'strokes': [
                {'direction': True, 'shape': True, 'count': False, 'shape_score': 5, 'size': True},
                {'direction': True, 'shape': True, 'count': True, 'shape_score': 10, 'size': True},
            ]
        }
        self.compare_and_assert(too_many_points_data, correct_data, expected_output)

    def test_too_many_points_template(self):
        expected_output = {
            'count': 0,
            'strokes': [
                {'direction': True, 'shape': True, 'count': False, 'shape_score': 10, 'size': True},
                {'direction': True, 'shape': True, 'count': True, 'shape_score': 10, 'size': True},
            ]
        }
        self.compare_and_assert(correct_data, too_many_points_data, expected_output)