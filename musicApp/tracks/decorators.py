def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run and wrapper.run_count < 15:
            wrapper.has_run = True
            wrapper.run_count += 1
            return f(*args, **kwargs)
    wrapper.has_run = False
    wrapper.run_count = 0
    return wrapper

