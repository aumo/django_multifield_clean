from __future__ import absolute_import

import pytest

from django.core.exceptions import FieldError

from multifieldclean.tests.test_app.forms import CustomPrefixForm, InvalidForm, MissingFieldTestForm, TestForm


'''
Note: it might have seemed to be a good idea to use the Mock
library to detect wether validation methods were called or not
but it cannot be done as Mock replaces patched methods by
MagicMock instances which obviously do not pas the inspect.is_method
check and don't support inspect.argspec .
'''


def form_error_codes(form):
    error_codes = []
    for _, errors in form.errors.as_data().items():
        error_codes.extend([e.code for e in errors if e.code])
    return error_codes


def test_validation_successes():
    form = TestForm(data={
        'field_1': 1,
        'field_2': 0,
    })

    assert form.is_valid()


def test_validation_fails():
    form = TestForm(data={
        'field_1': 1,
        'field_2': 2,
    })

    assert 'field_1_too_small' in form_error_codes(form)

    assert 'field_1_too_small_raised' in form_error_codes(form)


def test_missing_required_parameters():
    form = MissingFieldTestForm(data={'field_1': 1})  # field_2 missing
    form.is_valid()
    error_codes = form_error_codes(form)

    assert 'method_was_called_which_should_not_have' not in error_codes
    assert 'multi_clean_must_not_be_called' in [method_name for method_name, _ in form._collect_validation_config()]
    assert 'method_was_called_which_should_have' in error_codes
    assert form.field_2_default_value == 5


def test_validation_method_invalid_args():
    form = InvalidForm(data={'field': 0})

    with pytest.raises(FieldError) as field_error:
        form.is_valid()

    assert str(field_error.value) == 'Unknown field (not_a_field) specified for InvalidForm.multi_clean_wrong_arguments(self, field, not_a_field)'


def test_custom_method_prefix(settings):
    settings.MULTIFIELD_CLEAN_METHOD_PREFIX = 'custom_clean'

    form = CustomPrefixForm(data={'field': 1})
    form.is_valid()

    assert 'customly_prefixed_method_called' in form_error_codes(form)
