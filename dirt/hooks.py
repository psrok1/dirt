from functools import partial, wraps
from collections import defaultdict

registered_hooks = defaultdict(dict)


def hook(tag, target_fn):
    if not getattr(target_fn.callback, "hookable", False):
        raise RuntimeError("Hook can't be set - handler is not hookable")

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)
        target = target_fn.callback.__name__
        if tag not in registered_hooks[target]:
            registered_hooks[target] = {"pre": [], "post": []}
        registered_hooks[target][tag].append(wrapper)
        return wrapper
    return decorator


def hookable(fn):
    @wraps(fn)
    def hookable_target(*args, **kwargs):
        # Call pre-hooks
        if "pre" in registered_hooks[fn.__name__]:
            [hook(*args, **kwargs) for hook in registered_hooks[fn.__name__]["pre"]]
        # Call target
        fn(*args, **kwargs)
        # Call post-hooks
        if "post" in registered_hooks[fn.__name__]:
            [hook(*args, **kwargs) for hook in registered_hooks[fn.__name__]["post"]]
    setattr(hookable_target, "hookable", True)
    return hookable_target


pre_hook = partial(hook, 'pre')
post_hook = partial(hook, 'post')
