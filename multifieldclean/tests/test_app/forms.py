#!/usr/bin/env python
# coding: utf-8

from django import forms
from django.core.exceptions import ValidationError

from multifieldclean.forms import MultiFieldCleanFormMixin


class TestForm(MultiFieldCleanFormMixin, forms.Form):
    field_1 = forms.IntegerField()
    field_2 = forms.IntegerField()

    def multi_clean_field_1_greater_than_field_2(self, field_1, field_2):
        if field_1 <= field_2:
            self.add_error(None, ValidationError('error', code='field_1_too_small'))

    def multi_clean_field_1_greater_than_field_2_raises(self, field_1, field_2):
        if field_1 <= field_2:
            raise ValidationError('error', code='field_1_too_small_raised')


class MissingFieldTestForm(MultiFieldCleanFormMixin, forms.Form):
    field_1 = forms.IntegerField()
    field_2 = forms.IntegerField()

    def multi_clean_must_not_be_called(self, field_1, field_2):
        self.add_error(None, ValidationError('error', code='method_was_called_which_should_not_have'))

    def multi_clean_must_be_called(self, field_1, field_2=5):
        self.field_2_default_value = field_2
        self.add_error(None, ValidationError('error', code='method_was_called_which_should_have'))


class InvalidForm(MultiFieldCleanFormMixin, forms.Form):
    field = forms.IntegerField()

    def multi_clean_wrong_arguments(self, field, not_a_field):
        pass


class CustomPrefixForm(MultiFieldCleanFormMixin, forms.Form):
    field = forms.IntegerField()

    def custom_clean(self, field):
        self.add_error(None, ValidationError('error', code='customly_prefixed_method_called'))
