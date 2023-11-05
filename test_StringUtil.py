from PythonLib.StringUtil import StringUtil


def test1() -> None:
    assert StringUtil.isNubmer("5")
    assert StringUtil.isNubmer("50")
    assert StringUtil.isNubmer("50.0")
    assert not StringUtil.isNubmer("")
    assert StringUtil.isNubmer("   37".strip())
