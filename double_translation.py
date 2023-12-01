from coordinate import Coordinate
from translator import anchor_translate, gaussian_elimination2d
import numpy as np


def merge_coordinate(
    A_space_base: [Coordinate, Coordinate, Coordinate],
    B_space_base: [Coordinate, Coordinate, Coordinate],
    transition_space_base_A: [Coordinate, Coordinate, Coordinate],
    transition_space_base_B: [Coordinate, Coordinate, Coordinate],
    base_A_point: Coordinate,
):
    """base_A_point is a coordinate in the A space
    then it is translated to the transition space,
    and then via the transition space, it is translated to base B,
    and finally converted to the B space
    """
    # translate to transition space

    transition_space_point: Coordinate = anchor_translate(
        transition_space_base_A,
        A_space_base,
        base_A_point
    )

    # translate to base B
    base_B_point: Coordinate = anchor_translate(
        B_space_base,
        transition_space_base_B,
        transition_space_point
    )

    return base_B_point


if __name__ == '__main__':
    # same bases
    A_space_base = [Coordinate(0, 0), Coordinate(0, 10), Coordinate(10, 0)]
    B_space_base = [Coordinate(0, 0), Coordinate(0, 10), Coordinate(10, 0)]
    transition_space_base_A = [Coordinate(
        0, 0), Coordinate(0, 10), Coordinate(10, 0)]
    transition_space_base_B = [Coordinate(
        0, 0), Coordinate(0, 10), Coordinate(10, 0)]
    space_A_point = Coordinate(5, 5)
    base_B_point = merge_coordinate(
        A_space_base,
        B_space_base,
        transition_space_base_A,
        transition_space_base_B,
        space_A_point
    )
    assert np.all(np.isclose(space_A_point.tuple,
                  base_B_point.tuple))  # type: ignore

    # different bases
    A_space_base = [Coordinate(0, 0), Coordinate(0, 10), Coordinate(10, 0)]
    space_A_point = Coordinate(5, 5)
    # in A base, base_A_point should be (0.5,0.5)
    temp = gaussian_elimination2d(np.array([
        [
            A_space_base[1].x - A_space_base[0].x,
            A_space_base[2].x - A_space_base[0].x,
            space_A_point.x],
        [
            A_space_base[1].y - A_space_base[0].y,
            A_space_base[2].y - A_space_base[0].y,
            space_A_point.y
        ]
    ]))
    print(temp)
    assert np.all(np.isclose(temp, (0.5, 0.5)))  # type: ignore

    transition_space_base_A = [
        Coordinate(-2, 7), Coordinate(5, 12), Coordinate(1, 6)]
    # in transition space, base_A_point should be (3, 9)

    temp = Coordinate(
        transition_space_base_A[0].x + 0.5 * (transition_space_base_A[1].x - transition_space_base_A[0].x) + 0.5 * (
            transition_space_base_A[2].x - transition_space_base_A[0].x),
        transition_space_base_A[0].y + 0.5 * (transition_space_base_A[1].y - transition_space_base_A[0].y) + 0.5 * (
            transition_space_base_A[2].y - transition_space_base_A[0].y)
    )
    print(temp)
    assert np.all(np.isclose(temp.tuple, (3, 9)))  # type: ignore

    temp = anchor_translate(transition_space_base_A,
                            A_space_base, space_A_point)
    print(temp)
    assert np.all(np.isclose(temp.tuple, (3, 9)))  # type: ignore
    transition_space_base_B = [Coordinate(
        0, 0), Coordinate(0, 10), Coordinate(10, 0)]
    B_space_base = [Coordinate(0, 0), Coordinate(0, 10), Coordinate(10, 0)]
    # in B base, base_A_point should be (0.3, 0.9)
    # in B space, base_A_point should be (3, 9)
    base_B_point = merge_coordinate(
        A_space_base,
        B_space_base,
        transition_space_base_A,
        transition_space_base_B,
        space_A_point
    )
    print(base_B_point)
    assert np.all(np.isclose(base_B_point.tuple, (3, 9)))  # type: ignore

    # back and forth
    A_space_base = [Coordinate(
        15, -23), Coordinate(18, -22), Coordinate(14, -22)]
    space_A_point = Coordinate(7, 5)
    transition_space_base_A = [
        Coordinate(-1, 2), Coordinate(-9, 10), Coordinate(11, 0)]
    B_space_base = [Coordinate(-1, 9), Coordinate(-3, 10), Coordinate(2, 8)]
    transition_space_base_B = [Coordinate(
        0, 21), Coordinate(0, 10), Coordinate(10, 0)]
    base_B_point = merge_coordinate(
        A_space_base,
        B_space_base,
        transition_space_base_A,
        transition_space_base_B,
        space_A_point
    )
    print(base_B_point)
    space_A_point2 = merge_coordinate(
        B_space_base,
        A_space_base,
        transition_space_base_B,
        transition_space_base_A,
        base_B_point
    )
    assert np.all(np.isclose(space_A_point.tuple,
                  space_A_point2.tuple))  # type: ignore
