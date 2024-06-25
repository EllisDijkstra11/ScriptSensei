import unittest
import numpy as np
from kanji_class import Stroke, Kanji
import compare_kanji as kanji

# Sample data for testing
input_data = [
    [[0, 0], [1, 1]],  # First stroke of input kanji
    [[2, 2], [3, 3]]   # Second stroke of input kanji
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
        global input_data, template_data

        kanji.input_kanji = Kanji(input_data)
        kanji.template_kanji = Kanji(template_data)

    def test_scaling(self):
        tolerance = 1e-6
        kanji.compare_kanji(input_data, template_data)
        self.assertAlmostEqual(kanji.scale, 1, delta=tolerance)

        kanji.compare_kanji(input_data, wrong_data)
        self.assertAlmostEqual(kanji.scale, 3, delta=tolerance)

    def test_compare_kanji(self):
        global input_data, template_data, wrong_data

        kanji.compare_kanji(input_data, template_data)
        self.assertTrue(kanji.input_kanji.get_count())
        self.assertTrue(kanji.template_kanji.get_count())
        
        kanji.compare_kanji(input_data, wrong_data)
        self.assertFalse(kanji.input_kanji.get_count())
        self.assertTrue(kanji.template_kanji.get_count())

    def test_check_count(self):
        self.assertTrue(kanji.check_count())

        global input_data, wrong_data
        kanji.input_kanji = Kanji(input_data)
        kanji.template_kanji = Kanji(wrong_data)
        
        self.assertFalse(kanji.check_count())

    def test_check_count_vectors(self):
        input_stroke = kanji.input_kanji.get_stroke(0)
        template_stroke = kanji.template_kanji.get_stroke(0)

        self.assertTrue(kanji.check_count_vectors(input_stroke, template_stroke))

        global input_data, wrong_data
        kanji.input_kanji = Kanji(input_data)
        kanji.template_kanji = Kanji(wrong_data)

        input_stroke = kanji.input_kanji.get_stroke(0)
        template_stroke = kanji.template_kanji.get_stroke(0)

        self.assertFalse(kanji.check_count_vectors(input_stroke, template_stroke))

    def test_check_direction(self):
        input_stroke = kanji.input_kanji.get_stroke(0)
        template_stroke = kanji.template_kanji.get_stroke(0)

        self.assertTrue(kanji.check_direction(input_stroke, template_stroke))

        global input_data, wrong_data
        kanji.input_kanji = Kanji(input_data)
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