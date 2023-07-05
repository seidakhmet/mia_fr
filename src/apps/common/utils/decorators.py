import base64
import time
import uuid
from contextlib import contextmanager

from django.core.cache import caches
from redis.exceptions import ConnectionError

LOCK_EXPIRE = 60 * 10  # Lock expires in 10 minutes


def _argument_signature(*args, **kwargs):
    arg_list = [str(x) for x in args]
    kwarg_list = [f"{str(k)}:{str(v)}" for k, v in kwargs.items()]
    return base64.b64encode(f"{'_'.join(arg_list)}-{'_'.join(kwarg_list)}".encode()).decode()


@contextmanager
def _redis_lock(lock_name, expires=LOCK_EXPIRE):
    random_value = str(uuid.uuid4())
    timeout_at = time.monotonic() + LOCK_EXPIRE - 3
    redis_cache = caches["redis"]
    try:
        status = redis_cache.add(lock_name, random_value, expires)
    except ConnectionError:
        status = True
    try:
        yield status
    finally:
        if time.monotonic() < timeout_at and status:
            try:
                redis_cache.delete(lock_name)
            except ConnectionError:
                pass


def task_lock(func=None, main_key="", timeout=None):
    """Обеспечение выполнения задачи только по одной за раз."""

    def _dec(run_func):
        def _caller(*args, **kwargs):
            with _redis_lock(f"{main_key}_{_argument_signature(*args, **kwargs)}", timeout) as acquired:
                if not acquired:
                    return "Выполнение задачи пропущено — другая задача уже имеет блокировку"
                return run_func(*args, **kwargs)

        return _caller

    return _dec(func) if func is not None else _dec
