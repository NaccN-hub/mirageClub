from functools import wraps
from flask import g, abort


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        is_auth = getattr(g.user, 'Id_tipousuario', False)
        if not is_auth:
            abort(401)
        elif is_auth == 3:
            abort(403)
        return f(*args, **kws)
    return decorated_function
