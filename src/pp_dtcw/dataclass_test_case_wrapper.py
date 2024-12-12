import pytest
from typing import Any
from _pytest.mark import ParameterSet  # Need for ParameterSet type hinting.
from _collections_abc import Collection # Need for `marks` type hinting.
import logging

class DataclassTestCaseWrapper:
    """
    A class to wrap other classes using the `@dataclass` decorator for pytest test cases.
    Intended to be used with `rdy_entries_for_parametrization()` to prepare data for pytest parametrization.

    Example usage:

    .. code-block:: python
    
        from dataclasses import dataclass
        from dataclass_test_case_wrapper import DataclassTestCaseWrapper, rdy_entries_for_parametrization

        # Create a static method which we'll use to return the processed wrapped dataclass test cases.
        @staticmethod
        def is_identical_test_cases() -> tuple[str, list[tuple[Any] | ParameterSet]]:
            # Define the `@dataclass` format we want to use.
            @dataclass # NOTE: `@dataclass` variables REQUIRE type hinting.
            class IsIdenticalTestCase:
                bst_a: BST
                bst_b: BST
                expected_bool: bool | None = None

            # Define our parametrization entries.
            entries_for_parametrization = [
                # No id, no marks.
                DataclassTestCaseWrapper(dataclass=IsIdenticalTestCase(
                    bst_a=BST.build_BST([5]),
                    bst_b=BST.build_BST([5, 3]),
                    expected_bool=False
                )),
                # With id.
                DataclassTestCaseWrapper(id="Small trees different", dataclass=IsIdenticalTestCase(
                    bst_a=BST.build_BST([5]),
                    bst_b=BST.build_BST([5, 3]),
                    expected_bool=False
                )),
                # With marks.
                DataclassTestCaseWrapper(id="Small trees different", marks=[pytest.mark.xfail],
                                        dataclass=IsIdenticalTestCase(
                    bst_a=BST.build_BST([5]),
                    bst_b=BST.build_BST([5, 3]),
                    expected_bool=False
                )),
            ]

        # Process and return our parametrization entries.
        return rdy_entries_for_parametrization(entries_for_parametrization)

        # Expand the return values of our defined static method as parametrization arguments.
        @pytest.mark.parametrize(*is_identical_test_cases())
        def test_BST_is_identical(self, bst_a:BST, bst_b:BST, expected_bool:bool):
            is_identical:bool = BST.is_identical(bst_a.root, bst_b.root)
            assert is_identical == expected_bool
    """
    def __init__(self, dataclass, id:str|None = None, marks:pytest.MarkDecorator|Collection[pytest.MarkDecorator|pytest.Mark] = ()):
        """Type of `dataclass` is supposed to be unknown: can be any `@dataclass` class."""
        self.id:str|None = id
        self.marks:pytest.MarkDecorator|Collection[pytest.MarkDecorator|pytest.Mark] = marks
        self.dataclass = dataclass

def _get_all_var_keys(test_case:DataclassTestCaseWrapper) -> str:
    """Taking a dataclass test case wrapper, gets all variable names in the dataclass.

    :return: Comma-separated string of all var names in the dataclass.
    """
    test_cases_dict_keys:list[str] = list(test_case.dataclass.__dict__.keys())
    return ", ".join(test_cases_dict_keys)

def _rdy_entry_for_parametrization(test_case:DataclassTestCaseWrapper) -> tuple[Any] | ParameterSet:
    """See `rdy_dataclass_entries_for_parametrization()`.

    If test case has `.id` or `.marks` field, returned entry will be of type `ParameterSet`, otherwise `tuple`.
    """
    test_case_var_values:list[Any] = []

    # Put all values of the dataclass test case into a list.
    for test_case_var_name in test_case.dataclass.__dict__:
        test_case_var_val:Any = getattr(test_case.dataclass, test_case_var_name)
        test_case_var_values.append(test_case_var_val)

    # If id OR marks are present, turn parametrization entry into ParameterSet data type.
    # Note: `*values` object for `pytest.param()` must be separate values. E.g. `pyest.param(1, 2, 3)` or `pytest.param(*[1, 2, 3])`.
    if test_case.id or test_case.marks:
        if not (test_case.id): # No id means ONLY marks are present.
            ParameterSet_for_parametrization:ParameterSet = pytest.param(*test_case_var_values, marks=test_case.marks)
        elif not (test_case.marks): # No marks means ONLY id is present.
            ParameterSet_for_parametrization:ParameterSet = pytest.param(*test_case_var_values, id=test_case.id)
        else: # Both id and marks are present.
            ParameterSet_for_parametrization:ParameterSet = pytest.param(*test_case_var_values, id=test_case.id, marks=test_case.marks)

        return ParameterSet_for_parametrization
    else: # Return parametrization entry as tuple. Since no id or marks.
        return tuple(test_case_var_values)

def rdy_entries_for_parametrization(test_cases:list[DataclassTestCaseWrapper]) -> tuple[str, list[tuple[Any] | ParameterSet]]:
    """For each test case wrapper instance, process data into an entry that is then ready for parametrization with `@pytest.mark.parametrize()`.

    :param test_cases: List of DataclassTestCaseWrapper instances.
    :return: Tuple of two values: str containing all variable names in DataclassTestCaseWrapper & for each test case, data entries for parametrization.
    Returns empty tuple if no test cases provided.
    """
    if len(test_cases) == 0:
        logging.warning("No dataclass test cases provided for parametrization.")
        return ("", [])
    entries_for_parametrization:list[tuple[Any] | ParameterSet] = [] # List containing processed entries at end, ready to be passed into `@pytest.mark.parametrize()`.
    test_cases_dict_keys_joined:str = _get_all_var_keys(test_cases[0])
    logging.info(f"Parametrization keys: {test_cases_dict_keys_joined}")

    for i, test_case in enumerate(test_cases):
        entries_for_parametrization.append(
            _rdy_entry_for_parametrization(test_case)
        )
        logging.info(f"[{i}] vals: {entries_for_parametrization[-1]}")

    return (test_cases_dict_keys_joined, entries_for_parametrization)
