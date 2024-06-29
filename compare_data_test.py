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
            # self.assertEqual(input_stroke.get_shape(), expected_stroke['shape'])
            self.assertEqual(input_stroke.get_order(), expected_stroke['order'])
            # self.assertEqual(int(input_stroke.get_shape_score()), expected_stroke.get('shape_score', 0))

    def test_kanji_one(self):
        input_data = [[[105.5, 254], [456.5, 263]]]
        template_data = [[[11.0, 54.25], [20.73, 54.75], [89.31, 49.51], [96.88, 50.0]]]

        expected_output = {
            'count': 0,
            'size': 10,
            'strokes': [
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
            ]
        }
        self.compare_and_assert(input_data, template_data, expected_output)

    def test_kanji_two(self):
        input_data = [[[83, 110], [456, 118], [503, 111]], [[84, 409], [504, 410]]]
        template_data = [[[25.25, 32.4], [31.8, 32.769999999999996], [73.04, 29.009999999999998], [79.25, 29.369999999999997]], [[12.0, 80.75], [21.09, 81.25], [88.58, 76.51], [96.88, 77.0]]]

        expected_output = {
            'count': 0,
            'size': 10,
            'strokes': [
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': int(20/3)},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
            ]
        }
        self.compare_and_assert(input_data, template_data, expected_output)

    def test_kanji_two_order(self):
        # No location data is used, so this does not change the result
        input_data = [[[84, 409], [504, 410]], [[83, 110], [456, 118], [503, 111]]]
        template_data = [[[25.25, 32.4], [31.8, 32.769999999999996], [73.04, 29.009999999999998], [79.25, 29.369999999999997]], [[12.0, 80.75], [21.09, 81.25], [88.58, 76.51], [96.88, 77.0]]]

        expected_output = {
            'count': 0,
            'size': 10,
            'strokes': [
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': int(20/3)},
            ]
        }
        self.compare_and_assert(input_data, template_data, expected_output)

    def test_kanji_three(self):
        input_data = [[[85, 115], [451, 116], [452, 120]], [[75, 278], [487, 276]], [[97, 473], [448, 462]]]
        template_data = [[[27.5, 23.65], [36.9, 23.709999999999997], [75.87, 20.139999999999997], [85.01, 20.369999999999997]], [[28.75, 55.14], [38.39, 55.34], [73.12, 52.220000000000006], [81.25, 52.52]], [[13.0, 87.83], [24.75, 88.55], [85.87, 84.47999999999999], [96.62, 85.25999999999999]]]

        expected_output = {
            'count': 0,
            'size': 10,
            'strokes': [
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': int(20/3)},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
            ]
        }
        self.compare_and_assert(input_data, template_data, expected_output)

    def test_kanji_three_order(self):
        # No location data is used, so this does not change the result
        input_data = [[[85, 115], [451, 116], [452, 120]], [[97, 473], [448, 462]], [[75, 278], [487, 276]]]
        template_data = [[[27.5, 23.65], [36.9, 23.709999999999997], [75.87, 20.139999999999997], [85.01, 20.369999999999997]], [[28.75, 55.14], [38.39, 55.34], [73.12, 52.220000000000006], [81.25, 52.52]], [[13.0, 87.83], [24.75, 88.55], [85.87, 84.47999999999999], [96.62, 85.25999999999999]]]

        expected_output = {
            'count': 0,
            'size': 10,
            'strokes': [
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': int(20/3)},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
            ]
        }
        self.compare_and_assert(input_data, template_data, expected_output)

    def test_kanji_insect(self):
        input_data = [
            [[130, 186], [132, 287]],
            [[124, 188], [378, 185], [373, 282]],
            [[123, 279], [369, 277], [378, 274]],
            [[247, 91], [260, 448]],
            [[118, 456], [386, 411], [396, 411]],
            [[359, 361], [391, 444]]
        ]
        template_data = [[[23.64, 36.26], [25.34, 38.8], [28.72, 57.459999999999994], [29.5, 62.239999999999995]], [[25.76, 38.04], [79.5, 33.5], [83.13, 37.75], [79.06, 55.07]], [[30.0, 60.0], [74.75999999999999, 56.51], [80.55, 56.11]], [[52.51, 16.12], [54.18, 20.11], [54.22, 83.74000000000001]], [[22.75, 89.75], [27.0, 91.0], [81.75, 78.5]], [[74.96, 69.87], [89.46, 90.37]]]

        expected_output = {
            'count': 0,
            'size': 10,
            'strokes': [
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
            ]
        }
        self.compare_and_assert(input_data, template_data, expected_output)

    def test_kanji_day(self):
        input_data = [
            [[173, 158], [186, 442]],
            [[158, 157], [158, 157], [159, 157], [160, 157], [162, 157], [358, 160], [375, 433]],
            [[177, 298], [179, 299], [328, 300], [392, 302]],
            [[177, 441], [180, 442], [258, 437], [386, 433]]
        ]
        template_data = [[[31.75, 24.75], [33.24, 29.0], [33.24, 89.0]], [[34.48, 26.0], [74.5, 22.5], [79.5, 26.75], [79.01, 89.0]], [[33.72, 55.5], [55.97, 54.0], [63.19, 53.45]], [[33.98, 86.75], [78.78999999999999, 84.25]]]
        expected_output = {
            'count': 0,
            'size': 10,
            'strokes': [
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
            ]
        }
        self.compare_and_assert(input_data, template_data, expected_output)

    def test_kanji_ear(self):
        input_data = [[[122, 99], [454, 87]], [[183, 101], [169, 311]], [[119, 318], [428, 248]]]
        input_data = [
            [[102, 102], [438, 110]],
            [[162, 103], [158, 354]],
            [[161, 173], [399, 164]],
            [[159, 245], [396, 237]],
            [[118, 351], [406, 298]],
            [[396, 135], [409, 443]]
        ]
        template_data = [[[21.0, 20.25], [27.17, 20.75], [81.86, 15.01], [87.5, 15.5]], [[36.68, 22.5], [38.32, 27.23], [37.99, 69.25]], [[40.0, 35.5], [54.58, 34.0], [59.33, 33.45]], [[39.5, 51.25], [54.22, 49.87], [58.769999999999996, 49.37]], [[17.5, 71.0], [21.0, 72.5], [79.75, 61.75]], [[71.25, 18.5], [72.5, 22.0], [72.75, 95.5]]]

        expected_output = {
            'count': 0,
            'size': 10,
            'strokes': [
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
            ]
        }
        self.compare_and_assert(input_data, template_data, expected_output)

    def test_kanji_below(self):
        input_data = [
            [[125.5, 127], [127.5, 128], [524.5, 130], [526.5, 129]],
            [[317.5, 129], [318.5, 138], [325.5, 328], [328.5, 465]],
            [[413.5, 243], [415.5, 244], [465.5, 332], [464.5, 332]]
        ]
        template_data = [
            [[13.25, 22.5], [20.990000000000002, 23.25], [87.37, 18.5], [95.25, 19.75]],
            [[52.97, 23.25], [54.53, 28.55], [54.26, 85.75], [54.239999999999995, 94.0]],
            [[67.83, 37.17], [82.0, 52.12]]
        ]

        expected_output = {
            'count': 0,
            'size': 10,
            'strokes': [
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 5},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 5},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
            ]
        }
        self.compare_and_assert(input_data, template_data, expected_output)

    def test_kanji_big(self):
        input_data = [
            [[121.5, 217], [126.5, 219], [414.5, 215]],
            [[258.5, 119], [254.5, 293], [206.5, 378], [194.5, 392], [174.5, 409], [112.5, 431]],
            [[256.5, 238], [479.5, 461]]
        ]
        template_data = [[[19.38, 48.25], [26.979999999999997, 48.74], [77.19, 42.44], [84.5, 42.769999999999996]], [[49.5, 18.0], [50.49, 24.32], [18.0, 91.75]], [[49.5, 46.0], [86.99000000000001, 89.28], [94.00000000000001, 93.25]]]

        expected_output = {
            'count': 0,
            'size': 10,
            'strokes': [
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
            ]
        }
        self.compare_and_assert(input_data, template_data, expected_output)

    def test_kanji_mountain(self):
        # This test is going wrong, but absolutely no idea why
        input_data = [
            [[277, 55], [277, 58], [279, 392], [280, 440]],
            [[88, 267], [89, 270], [82, 434], [517, 417]],
            [[495, 243], [496, 247], [493, 416]]
        ]
        template_data = [
            [[52.49, 15.5], [54.75, 21.25], [54.5, 80.5]],
            [[21.49, 54.5], [22.75, 58.25], [20.25, 81.25], [22.25, 85.0], [87.75, 79.0]],
            [[89.24, 49.0], [90.75, 53.25], [88.2, 82.02], [87.75, 87.0]]
            ]

        expected_output = {
            'count': 0,
            'size': 10,
            'strokes': [
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10}
            ]
        }
        self.compare_and_assert(input_data, template_data, expected_output)

        input_data = [
            [
                [265, 81], [260, 112], [97, 272], [90, 273]
            ],
            [
                [259, 109], [262, 111], [408, 244], [450, 294]
            ],
            [
                [204, 209], [309, 206]
            ],
            [
                [151, 268], [378, 262]
            ],
            [
                [261, 215], [262, 217], [264, 423]
            ],
            [
                [148, 324], [150, 325], [183, 365], [186, 367]
            ],
            [
                [370, 331], [367, 334], [337, 362], [302, 365]
            ],
            [
                [113, 423], [134, 423], [231, 421], [447, 421]
            ]
        ]
        template_data = [[[51.75, 11.88], [50.95, 16.72], [14.5, 58.0]], [[52.25, 18.25], [89.46000000000001, 50.92], [95.00000000000001, 53.75]], [[34.02, 47.08], [39.620000000000005, 47.29], [63.61, 44.65], [69.76, 44.769999999999996]], [[30.18, 64.96], [36.65, 65.08], [68.0, 62.55], [74.96, 62.629999999999995]], [[51.47, 48.82], [52.36, 53.25], [52.58, 93.07]], [[31.0, 74.75], [39.5, 86.75]], [[73.01, 72.11], [72.47, 75.62], [63.0, 86.0]], [[18.5, 94.86], [27.869999999999997, 95.01], [79.38, 92.01], [88.75999999999999, 92.60000000000001]]]

        expected_output = {
            'count': 0,
            'size': 10,
            'strokes': [
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
            ]
        }
        self.compare_and_assert(input_data, template_data, expected_output)

    def test_kanji_life(self):
        input_data = [
            [[164, 80], [162, 83], [161, 130], [92, 224]],
            [[165, 152], [427, 158]],
            [[294, 51], [310, 516]],
            [[129, 308], [463, 299], [474, 297]],
            [[68, 500], [487, 468]]
        ]
        template_data = [
            [[31.02, 27.14], [30.95, 29.42], [19.0, 51.25]],
            [[30.88, 40.92], [34.48, 41.300000000000004], [74.84, 33.92], [77.87, 33.9]],
            [[30.88, 64.53], [34.48, 64.81], [75.84, 59.39], [78.87, 59.37]],
            [[17.88, 91.25], [23.5, 91.55], [85.02000000000001, 85.75], [91.75000000000001, 86.73]],
            [[51.81, 12.88], [54.32, 17.86], [54.07, 87.88]]
        ]

        expected_output = {
            'count': 0,
            'size': 10,
            'strokes': [
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 2, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': -2, 'shape_score': 10},
            ]
        }
        self.compare_and_assert(input_data, template_data, expected_output)

    def test_kanji_enter(self):
        input_data = [
            [[268, 272], [94, 466]],
            [[125, 127], [129, 128], [462, 448]]
        ]
        template_data = [[[54.75, 48.75], [52.68, 53.37], [14.5, 88.0]], [[36.5, 20.0], [85.31, 82.08], [94.75, 88.5]]]

        expected_output = {
            'count': 0,
            'size': 10,
            'strokes': [
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
            ]
        }
        self.compare_and_assert(input_data, template_data, expected_output)

    def test_kanji_child(self):
        input_data = [
            [
                [147, 100], [151, 105], [262, 119], [313, 111],
                [314, 152], [270, 191], [240, 221]
            ],
            [
                [240, 224], [291, 487], [289, 489], [287, 491], [208, 445]
            ],
            [
                [99, 288], [105, 288], [172, 281], [462, 289]
            ]
        ]
        template_data = [
            [[33.28, 19.04], [38.68, 19.669999999999998], [68.53999999999999, 14.749999999999998], [70.64999999999999, 18.33], [54.29999999999999, 35.519999999999996]],
            [[52.48, 37.74], [57.72, 90.31], [47.25, 91.3]],
            [[12.25, 51.48], [24.73, 51.97], [83.26, 45.22], [96.37, 45.79]]
            ]

        expected_output = {
            'count': 0,
            'size': 10,
            'strokes': [
                {'direction': False, 'shape': False, 'order': None, 'shape_score': 0},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
                {'direction': True, 'shape': True, 'order': 0, 'shape_score': 10},
            ]
        }
        self.compare_and_assert(input_data, template_data, expected_output)
    
