# Django multi field form validation

<https://github.com/aumo/django_multifield_clean>

Provides a Django form mixin that allows declaring validation methods 
(similar to the Django `Form.clean_<field_name>()` methods) working on multiple 
fields, allowing less boilerplate code in `Form.clean()`.


*Tested on Django 1.7, 1.8 and Python 2.7, 3.2, 3.3, 3.4*


## Installation

`pip install django_multifield_clean`

## Usage

Make your form inherit from the `multifieldclean.forms.MultiFieldCleanFormMixin` mixin. Note that the mixin must come **before** the Django form class.


Declare methods starting with `MULTIFIELD_CLEAN_METHOD_PREFIX` (default is `multi_clean`) which arguments are named after field names.

Those methods will be called during the form validation process, after `Form.clean()`, with the field values their arguments are named after as parameters.

If an argument has no default value, the validation method is called only if the field it is refering to has a value.

Example:


    from django import forms
    from django.core.exceptions import Validationerror

    from multifieldclean.forms import MultiFieldCleanFormMixin
    
    
    # The mixin must be placed before 'forms.Form'
    # so it can override its methods.
    class HolidaysForm(MultiFieldCleanFormMixin, forms.Form):
        start = forms.IntegerField()
        end = forms.IntegerField()
        
        # Any method starting with "multiclean" will be
        # interpreted as a multi field validation method.
        # The method will only be called only if 'start' and
        # 'end' have values.
        def multiclean_holidays_end_after_they_start(self, start, end):
           if start > end:
               self.add_error('end', 
                              ValidationError('These holidays end before they even start!'))
                              
         
 

 
            
            
### Configuration

* `MULTIFIELD_CLEAN_METHOD_PREFIX`: modify the prefix used to detect validation methods, default is `multiclean`.

## Why?

I often found myself writing a lot of boilerplate code when overriding the `Form.clean()` method, for example:

    def clean(self):
        start = self.cleaned_data.get('start')
        end = self.cleaned_data.get('end')
        if start and end:
            if start > end:
                # etc...
                
It is boring to write and harder to read. This package tries to provide a solution to this issue.


## Contributing

Pull requests are welcome.

Runnig the tests:

* To run the full suite, use `tox`.
* To run them for your current environment:
  * Install test requirements `pip install -r test-requirements.txt`
  * Install the targeted Django version.
  * Run `py.test`
  * Use `py.test --cov multifieldclean` to get the coverage report.
