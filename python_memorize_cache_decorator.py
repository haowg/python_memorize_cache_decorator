# coding: utf8

import time
import hashlib
from functools import wraps


def memorize(duration=-1):
    '''''自动缓存'''

    _cache = {}

    def _is_obsolete(entry, duration):
        '''''是否过期'''
        if duration == -1:  # 永不过期
            return False
        return time.time() - entry['time'] > duration

    def _compute_key(function, args, kwargs):
        '''''序列化并求其哈希值'''
        return hashlib.sha1(
            ''.join((str(function.func_name), str(args), str(kwargs)))
        ).hexdigest()

    def _memoize(function):
        @wraps(function)  # 自动复制函数信息
        def __memoize(*args, **kw):
            key = _compute_key(function, args, kw)
            # 是否已缓存？
            if key in _cache:
                # 是否过期？
                if not _is_obsolete(_cache[key], duration):
                    return _cache[key]['value']
                else:
                    # 如果有过期的数据清理一次缓存
                    for key in _cache.keys():
                        _is_obsolete(_cache[key], duration) and _cache.pop(key)
            # 运行函数
            result = function(*args, **kw)
            # 保存结果
            if result is not None:
                _cache[key] = {'value': result, 'time': time.time()}
            return result

        return __memoize

    return _memoize


@memorize(3)
def main(*args):
    return time.time()


if __name__ == "__main__":
    while True:
        print main()
        time.sleep(1)
