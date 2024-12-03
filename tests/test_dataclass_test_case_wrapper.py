import pytest
from dataclasses import dataclass # NOTE: `@dataclass` variables REQUIRE type hinting.
from pp_dtcw.dataclass_test_case_wrapper import DataclassTestCaseWrapper, rdy_entries_for_parametrization

class TestWrapper:
    @staticmethod
    def my_wrapper_test_cases():
        @dataclass
        class MyWrapperTestCase:
            str_a: str
            int_b: int
            float_c: float
            expected_bool: bool | None = None

        entries_for_parametrization = [
            DataclassTestCaseWrapper(dataclass=MyWrapperTestCase(
                str_a="one", int_b=1, float_c=1.0, expected_bool=True
            )),
            DataclassTestCaseWrapper(dataclass=MyWrapperTestCase(
                str_a="two", int_b=2, float_c=2.0, expected_bool=False
            )),
            DataclassTestCaseWrapper(dataclass=MyWrapperTestCase(
                str_a="three", int_b=3, float_c=3.0, expected_bool=True
            )),
            DataclassTestCaseWrapper(id="4", dataclass=MyWrapperTestCase(
                str_a="four", int_b=4, float_c=4.0, expected_bool=False
            )),
            DataclassTestCaseWrapper(id="5", marks=[pytest.mark.xfail],
                                        dataclass=MyWrapperTestCase(
                str_a="five", int_b=5, float_c=5.0, expected_bool=True
            )),
        ]

        return rdy_entries_for_parametrization(entries_for_parametrization)

    @pytest.mark.parametrize(*my_wrapper_test_cases())
    def test_wrapper(
        self,
        str_a: str,
        int_b: int,
        float_c: float,
        expected_bool: bool | None,
    ):
        print(f"str_a: {str_a}, int_b: {int_b}, float_c: {float_c}, expected_bool: {expected_bool}")
