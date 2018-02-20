import numpy as np
import unittest
import matplotlib.pyplot as plt
import mynavigatorhelpers as navh
import math

class InterpolationTests(unittest.TestCase):
    def test_unclamped_knot_vector(self):

        points = [
            [-1.0,  0.0],
            [-0.5,  0.5],
            [ 0.5, -0.5],
            [ 1.0,  0.0]
        ]

        degree = 2

        # As we don't provide a knot vector, one will be generated 
        # internally and have the following form :
        
        # knots = [0, 1, 2, 3, 4, 5, 6];
        
        # Knot vectors must have `number of points + degree + 1` knots.
        # Here we have 4 points and the degree is 2, so the knot vector 
        # length will be 7.
        
        # This knot vector is called "uniform" as the knots are all spaced uniformly,
        # ie. the knot spans are all equal (here 1).

        line = []
        for t in np.arange(0, 1, 0.01):
            line.append(navh.interpolation(t, points, degree))
        x = [i[0] for i in line]
        y = [i[1] for i in line]
        plt.figure()
        plt.scatter([i[0] for i in points], [i[1] for i in points])
        plt.plot(x,y)
        plt.show()


    def test_circle(self):
        """
        """
        points =  [
            [ 0.0, -0.5],
            [-0.5, -0.5],

            [-0.5,  0.0],
           [-0.5,  0.5],

            [ 0.0,  0.5],
            [ 0.5,  0.5],

            [ 0.5,  0.0],
            [ 0.5, -0.5],
            [ 0.0, -0.5]
        ]
        knots = [
            0, 0, 0, 1/4, 1/4, 1/2, 1/2, 3/4, 3/4, 1, 1, 1
        ]
        w = math.pow(2, 0.5) / 2
        weights = [
            1, w, 1, w, 1, w, 1, w, 1]
        degree = 2
        line = []
        for t in np.arange(0, 1, 0.01):
            line.append(navh.interpolation(t, points, degree, knots, weights))
        x = [i[0] for i in line]
        y = [i[1] for i in line]
        plt.figure()
        plt.scatter([i[0] for i in points], [i[1] for i in points])
        plt.plot(x,y)
        plt.show()

    def test_path_points(self):
        points = [(50.0, 50.0), (430, 58), (445, 197), (375.0, 230.0)]
        
        w = math.pow(2, 0.5) / 2
        knots = [
            0, 0, 0, 1, 2, 2, 2
        ]
        degree = 2
        line = []
        for t in np.arange(0, 1, 0.01):
            line.append(navh.interpolation(t, points, degree, knots))
        x = [i[0] for i in line]
        y = [i[1] for i in line]
        plt.figure()
        plt.scatter([i[0] for i in points], [i[1] for i in points])
        plt.plot(x,y)
        plt.show()



if __name__ == '__main__':
    interpolation_tests = unittest.TestLoader().loadTestsFromTestCase(InterpolationTests)
    unittest.TextTestRunner(verbosity=1).run(interpolation_tests)
