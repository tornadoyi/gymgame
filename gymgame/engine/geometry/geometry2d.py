from ..base import *

def raycast(origin, direct, distance, objs):
    objs = objs if isinstance(objs, (list, tuple)) else [objs]
    ray = Line2(origin, origin + direct.normalized * distance)

    min_cross_point = None
    min_cross_distance = np.inf

    def _update(point):
        nonlocal min_cross_point, min_cross_distance
        if point is None: return
        d = point.distance(origin)
        if d >= min_cross_distance: return
        min_cross_point = point
        min_cross_distance = d

    def _raycast_to_line(o):
        nonlocal min_cross_point, min_cross_distance
        point = ray.cross_point(o)
        _update(point)

    def _raycast_to_bounds(o):
        nonlocal min_cross_point, min_cross_distance
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

    return min_cross_point
