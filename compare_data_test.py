import unittest
import numpy as np
from kanji_class import Stroke, Kanji
import compare_kanji as kanji

class TestDataKanji(unittest.TestCase):

    def setUp(self):
        pass

    def compare_and_assert(self, input_data, template_data, expected_output):
        kanji.compare_kanji(input_data, template_data)
        
        self.assertEqual(kanji.input_kanji.get_count(), expected_output['count'])
        self.assertEqual(kanji.input_kanji.get_size(kanji.size_tolerance), expected_output['size'])

        for i, expected_stroke in enumerate(expected_output['strokes']):
            input_stroke = kanji.input_kanji.get_stroke(i)

            self.assertEqual(input_stroke.get_direction(), expected_stroke['direction'])
            self.assertEqual(input_stroke.get_shape(), expected_stroke['shape'])
            self.assertEqual(input_stroke.get_order(), expected_stroke['order'])
            self.assertEqual(input_stroke.get_shape_score(), expected_stroke.get('shape_score', 0))

    def test_kanji_one(self):
        input_data = [[[105.5, 254], [456.5, 263]]]
        template_data = [[[11.0, 54.25], [20.73, 54.75], [89.31, 49.51], [96.88, 50.0]]]

        expected_output = {
            'count': True,
            'size': 1,
            'strokes': [
                {'direction': True, 'shape': True, 'order': True, 'shape_score': 10},
            ]
        }
        self.compare_and_assert(input_data, template_data, expected_output)
