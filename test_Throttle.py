import time

from PythonLib.Throttle import Throttle


def test1() -> None:
    throttle = Throttle(3000)

    assert throttle.triggerAndCheck() is True
    time.sleep(1)
    assert throttle.triggerAndCheck() is False
    time.sleep(1)
    assert throttle.triggerAndCheck() is False
    time.sleep(1)
    assert throttle.triggerAndCheck() is True
    time.sleep(1)
    assert throttle.triggerAndCheck() is False
    time.sleep(1)
    assert throttle.triggerAndCheck() is False
    time.sleep(1)
    assert throttle.triggerAndCheck() is True


test1()
