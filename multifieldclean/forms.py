#!/usr/bin/env python
# coding: utf-8

'''
TODO maybe use metaclasses to build the validation config at parse time.
'''

from inspect import getargspec, getmembers, isfunction, ismethod

from django.core.exceptions import FieldError, ValidationError

from multifieldclean.settings import setting


__all__ = ['MultiFieldCleanFormMixin']


class MultiFieldCleanFormMixin(object):
    def _post_clean(self):
        '''
        Runs all multi field validation methods as collected by
        `_collect_validation_config` if their required fields are
        present in the form's cleaned data.
        '''
        self.clean_multifield()
        super(MultiFieldCleanFormMixin, self)._post_clean()

    def clean_multifield(self):
        for method_name, fields in self._collect_validation_config():
            run_validation = True
            kwargs = {}

            for field_name, required in fields:
                if self.cleaned_data.get(field_name) is not None:
                    kwargs[field_name] = self.cleaned_data[field_name]
                elif required:
                    run_validation = False
                    break

            if run_validation:
                try:
                    getattr(self, method_name)(**kwargs)
                except ValidationError as e:
                    self.add_error(None, e)

    def _collect_validation_config(self):
        '''
        Inspects the class' methods to find methods that should be
        used to validate the form based on multiple fields.

        Those methods' are those which names start with `multi_clean_`.

        Returns a "validation config" which a list of 2-elements tuples
        the first being the method's name the second a list of tuples
        describing the fields it takes as arguments. The first element
        of the field tuple is the field's name, the second, wether it is
        a required argument or not for this method.
        '''
        config = []

        # Need to check for isfunction or is
        methods = getmembers(
            self.__class__,
            predicate=lambda x: ismethod(x) or isfunction(x)
        )

        for method_name, method in methods:
            if not method_name.startswith(setting('METHOD_PREFIX')):
                continue
            argspec = getargspec(method)
            args = argspec.args[1:]  # Get rid of self.
            defaults_len = len(argspec.defaults) if argspec.defaults else 0
            required_args_count = len(args) - defaults_len

            fields = []
            for i, arg_name in enumerate(args):
                if not arg_name in self.fields:
                    raise FieldError(
                        'Unknown field ({}) specified for {}.{}({})'
                        .format(arg_name, self.__class__.__name__,
                                method_name, ', '.join(argspec.args)))

                required = i < required_args_count
                fields.append((arg_name, required, ))

            config.append((method_name, fields, ))

        return config
