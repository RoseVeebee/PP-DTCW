# PP-DTCW
Pytest Parametrization-Dataclass Test Case Wrapper<br>
*Tested with pytest 8.3.4.*

## tl;dr
Provides a way to expose @dataclass variables to `@pytest.mark.parametrize()` default id generation.

## Example usage
See the docstring of the `DataclassTestCaseWrapper` class in `./src/pp_dtcw/_dataclass_test_case_wrapper.py`.

## Detailed info
Pytest parametrization, using `@pytest.mark.parametrize()`, supports default id generation when no explicit id is given. However, if any of the `argvalues` is a 'complex' object, e.g. a class`, pytest default id generation will simply yield the name of the object followed by an increasing number based on the number of that object we're parametrizing.

In the example code below, pytest will generate default ids `test_case1`, `test_case2`, `test_case3` respectively.
```python
class TestCase:
    def __init__(self, val1:int, val2:int, str1:str):
        self.val1:int = val1
        self.val2:int = val2
        self.str1:str = str1

test_cases:list[TestCase] = [
    TestCase(1, 2, "a"),
    TestCase(3, 4, "b"),
    TestCase(5, 6, "c"),
]

@pytest.mark.parametrize("test_case", test_cases)
def test_quick_test(self, test_case:TestCase):
    print(test_case)
```