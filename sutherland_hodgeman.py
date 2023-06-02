import copy


def intersection_point(p1: tuple[float, float], p2: tuple[float, float], pi: tuple[float, float], pk: tuple[float, float]) -> tuple[float, float]:
    numx = (p1[0]*p2[1] - p1[1]*p2[0]) * (pi[0] - pk[0]) - \
        (p1[0]-p2[0]) * (pi[0]*pk[1] - pi[1]*pk[0])

    numy = (p1[0]*p2[1] - p1[1]*p2[0]) * (pi[1] - pk[1]) - \
        (p1[1]-p2[1]) * (pi[0]*pk[1] - pi[1]*pk[0])

    den = (p1[0] - p2[0]) * (pi[1]-pk[1]) - (p1[1]-p2[1]) * (pi[0]-pk[0])

    return (numx/den, numy/den)


def is_inside(p: tuple[float, float], p1: tuple[float, float], p2: tuple[float, float]) -> bool:
    result = (p2[0] - p1[0]) * (p[1]-p1[1]) - (p2[1] - p1[1]) * (p[0]-p1[0])

    return result < 0


def clip(points: list[tuple[float, float]], p1: tuple[float, float], p2: tuple[float, float]) -> list[tuple[float, float]]:
    result = []

    for i in range(len(points)):
        k = (i+1) % len(points)

        i_inside = is_inside(points[i], p1, p2)
        k_inside = is_inside(points[k], p1, p2)

        if i_inside and k_inside:
            result.append(points[k])
        elif not i_inside and k_inside:
            result.append(intersection_point(p1, p2, points[i], points[k]))
            result.append(points[k])
        elif i_inside and not k_inside:
            result.append(intersection_point(p1, p2, points[i], points[k]))

    return result


def sutherland_hodgeman(points: list[tuple[float, float]], clipper: list[tuple[float, float]]) -> list[tuple[float, float]]:
    result = copy.deepcopy(points)

    for i in range(len(clipper)):
        k = (i+1) % len(clipper)

        result = clip(result, clipper[i], clipper[k])

    return result
