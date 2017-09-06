from ..base import *

def _raycast(origin, direct, distance, objs):
    objs = objs if isinstance(objs, (list, tuple)) else [objs]
    ray = Line2(origin, origin + direct.normalized * distance)

    points = []
    min_point, max_point = None, None
    min_distance, max_distance = np.inf, -1

    def _update(point):
        nonlocal points, min_point, max_point, min_distance, max_distance
        if point is None: return
        d = point.distance(origin)
        if d < min_distance:
            min_point = point
            min_distance = d
        
        if d > max_distance:
            max_point = point
            max_distance = d

        points.append(point)


    def _raycast_to_line(o):
        nonlocal points, min_point, max_point, min_distance, max_distance
        point = ray.cross_point(o)
        _update(point)

    def _raycast_to_bounds(o):
        nonlocal points, min_point, max_point, min_distance, max_distance
        min, max = o.min, o.max
        lines = [
            Line2(min, Vector2(min.x, max.y)),
            Line2(min, Vector2(max.x, min.y)),
            Line2(Vector2(min.x, max.y), max),
            Line2(Vector2(max.x, min.y), max),
        ]
        for line in lines:
            _raycast_to_line(line)

    for o in objs:
        if isinstance(o, Line2):_raycast_to_line(o)
        elif isinstance(o, Bounds2):_raycast_to_bounds(o)
        else: raise Exception('unsupported geometry type {0}'.format(type(o)))

    return points, min_point, max_point


def raycast_all(*args, **kwargs): return _raycast(*args, **kwargs)[0]

def raycast_min(*args, **kwargs): return _raycast(*args, **kwargs)[1]

def raycast_max(*args, **kwargs): return _raycast(*args, **kwargs)[2]

def raycast(*args, **kwargs): return raycast_min(*args, **kwargs)