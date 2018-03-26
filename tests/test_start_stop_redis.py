import unittest

from rediscontroller import is_redis_running, start_redis, stop_redis


class TestStringMethods(unittest.TestCase):

    def test_default_parameters(self):
        start_redis(data_directory='./data')
        assert is_redis_running()
        stop_redis()

    def test_custom_port(self):
        redis_port = 12345
        start_redis(data_directory='./data', redis_port=redis_port)
        assert is_redis_running(redis_port=redis_port)
        stop_redis(redis_port=redis_port)

    def test_random_port(self):
        redis_port = start_redis(data_directory='./data', redis_port='random')
        assert is_redis_running(redis_port=redis_port)
        stop_redis(redis_port=redis_port)

    def test_wrong_port_argument(self):
        with self.assertRaises(AssertionError):
            start_redis(data_directory='./data', redis_port='wrong')

    def test_wrong_port_argument1(self):
        with self.assertRaises(AssertionError):
            start_redis(data_directory='./data', redis_port=1.0)


if __name__ == '__main__':
    unittest.main()
