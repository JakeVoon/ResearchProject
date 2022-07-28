# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import matplotlib.pyplot as plt
import numpy as np

file = 'data/max_pulling.json'


def load_experiment(json_file):
    try:
        # Opening JSON file
        with open(json_file) as json_file:

            experiment_json = json.load(json_file)['data'][15]
            curvature = experiment_json['curvatures']
            positions_2d = np.array(experiment_json['positions_2d'])
            positions_3d = np.array(experiment_json['positions_3d'])

    except json.JSONDecodeError:
        print('JSON is not rightly formatted')
    return experiment_json, curvature, positions_2d, positions_3d


def get_3_points_from_idx(idx_first_point):
    p1, p2, p3 = np.array(positions_2d[idx_first_point:idx_first_point + 3])
    return p1, p2, p3


def get_curvature_from_3_points(first_pos_id: int = 12):
    """ Compute curvature from the formula found https://en.wikipedia.org/wiki/Menger_curvature#Definition """
    p1, p2, p3 = get_3_points_from_idx(first_pos_id)

    p1x, p1y = p1
    p2x, p2y = p2
    p3x, p3y = p3

    aire_triangle = (p3x - p1x) * (p2y - p1y) / 2
    denum = np.linalg.norm(p1 - p2) * np.linalg.norm(p2 - p3) * np.linalg.norm(p3 - p1)

    curvature = 4 * aire_triangle / denum

    return curvature


def get_theta_from_3_points(first_pos_id: int = 12):
    """ Compute tetra from the formula found """
    p1, p2, p3 = get_3_points_from_idx(first_pos_id)

    p1x, p1y = p1
    p2x, p2y = p2
    p3x, p3y = p3

    a = (p1x - p2x, p1y - p2y)
    b = (p1x - p3x, p1y - p3y)

    theta = np.arccos(np.dot(a, b) / (np.dot(a, a) * np.dot(b, b)))
    return theta


def generate_curvature_array(positions_2d):
    calculated_curvature_array = []
    for i in range(len(positions_2d) - 3):
        kappa = get_curvature_from_3_points(positions_2d, i)
        calculated_curvature_array.append(kappa)

    return calculated_curvature_array


def display_everything(positions_2d, idx=10):
    positions_array = np.array(positions_2d)
    positions_2d_x = positions_array[:, 0]
    positions_2d_y = positions_array[:, 1]
    plt.plot(positions_2d_x, positions_2d_y)

    # for i in range(len(positions_2d) - 3):
    #     display_curvature_circle(positions_2d, i)

    display_curvature_circle(positions_2d, idx)

    show_tangente(positions_2d, idx)

    plt.axis('equal')
    plt.show()


def display_curvature_circle(positions_2d, id=8):
    k = get_curvature_from_3_points(positions_2d, id)
    r = np.abs(1 / k)

    p1, p2, p3 = np.array(positions_2d[id + 1:id + 4])
    point = [p1, p2, p3]

    # To display the points
    for p in point:
        px, py = p[0], p[1]
        plt.scatter(px, py, marker='+', s=50, c='r')

    Drawing_uncolored_circle = plt.Circle((p2[0], p2[1] + np.sign(k) * r), r, fill=False)

    ax = plt.gca()
    ax.add_artist(Drawing_uncolored_circle)


def compute_derivative(positions_2d, plot='off'):
    # Variable initialization
    x = positions_2d[:, 0]
    y = positions_2d[:, 1]
    nbx = len(x)
    yp = np.zeros(nbx - 1)

    # Compute the derivative
    xp = x[0:nbx - 1]
    for i in range(nbx - 1):
        yp[i] = (y[i + 1] - y[i]) / (x[i + 1] - x[i])

    if plot == 'on':
        plt.plot(x, y, label="f(x)")
        plt.plot(xp, yp, label="f'(x)")

        plt.legend()

    return yp


def show_affine(a=1, b=0, normal='no'):
    x = np.linspace(0, 25, 1000)
    # if normal != 'yes':
    #     x = np.linspace(0, 25, 1000)
    # else:
    #     x = np.linspace(11, 13, 1000)
    y = a * x + b

    plt.plot(x, y)

    return x, y


def show_tangente(positions_2d, idx):
    # Variable initialization
    x = positions_2d[:-1, 0]
    y = positions_2d[:, 1]

    derivative = compute_derivative(positions_2d)

    tan_a = derivative[idx]
    tan_b = y[idx + 1] + x[idx + 1] * derivative[idx]
    xt, yt = show_affine(tan_a, tan_b)

    normal_a = -1 / tan_a
    normal_b = tan_b / tan_a
    show_affine(normal_a, normal_b, 'yes')

    find_center(normal_a, normal_b, x, y, idx)


def find_center(normal_a, normal_b, x, y, idx):
    k = get_curvature_from_3_points(positions_2d, idx)
    r = np.abs(1 / k)

    x2, y2 = x[idx + 1], y[idx + 1]
    a = (1 + normal_a) ** 2
    b = 2 * normal_a + normal_b - 2 * x2 - 2 * normal_a * y2
    c = x2 ** 2 + y2 ** 2 + normal_b + r ** 2

    delta = b ** 2 - 4 * a * c
    s1_x = (-b + np.sqrt(np.abs(delta))) / (2 * a)
    s2_x = (-b - np.sqrt(np.abs(delta))) / (2 * a)

    s1_y = normal_a * s1_x + normal_b
    s2_y = normal_a * s2_x + normal_b

    plt.scatter(s1_x, s1_y)
    plt.scatter(s2_x, s2_y)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    experiment_json, curvature, positions_2d, positions_3d = load_experiment(file)
    # # k = generate_curvature_array(positions_2d)
    t = get_theta_from_3_points(16)
    print(t, np.degrees(t))
    # display_everything(positions_2d)
    # derivative = compute_derivative(positions_2d)
    # show_affine()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
