"""
#   AUTHOR      :   Robert James Patterson
#   DATE        :   06/11/17
#   LASTMOD     :   06/13/17
#   FILENAME    :   shipping.py
#   SYNOPSIS    :   Course work file for the Properties and Class Methods module of the
#                   'Beyond Basics' python.
"""
import iso6346


class ShippingContainer:

    HEIGHT_FT = 8.5
    WIDTH_FT = 8.0

    # 'next_serial' is an example of a Class attribute. This is
    # a property that is shared by ALL instances of this class.
    next_serial = 1337

    @staticmethod
    def _make_bic_code(owner_code, serial):
        return iso6346.create(owner_code=owner_code,
                              # We use the method 'zfile' on the
                              # 'serial' to ensure that it is at
                              # least 6 digits long.
                              serial=str(serial).zfill(6))

    # Code to use the @classmethod decorator, 'cls' is to class what
    # 'self' is to the instance and plays same role as self does
    # for the instance.
    @classmethod
    def _get_next_serial(cls):
        result = cls.next_serial
        # Modify the shared class attribute
        cls.next_serial += 1
        return result

    @classmethod
    def create_empty(cls, owner_code, length_ft, *args, **kwargs):
            return cls(owner_code, length_ft, contents=None, *args, **kwargs)

    @classmethod
    def create_with_items(cls, owner_code, length_ft, items, *args, **kwargs):
        return cls(owner_code, length_ft, contents=list(items), *args, **kwargs)

    def __init__(self, owner_code, length_ft, contents):
        """ Constructor """
        self.contents = contents
        self.length_ft = length_ft
        # Assign the shared class attribute to the instance. Notice
        # that we refer to the class and not the instance self, this
        # is vital to maintaining the Zen of Python.
        self.bic = self._make_bic_code(
            owner_code=owner_code,
            serial=ShippingContainer._get_next_serial())
    # This property demonstrates how properties are inherited
    # by children classes of this class.

    @property
    def volume_ft3(self):
        return ShippingContainer.HEIGHT_FT * ShippingContainer.WIDTH_FT * self.length_ft

##################################################################################################


# The class 'RefrigeratedShippingContainer' shows us how inherited
# static methods can be overridden in the child class.
class RefrigeratedShippingContainer(ShippingContainer):

    MAX_CELSIUS = 4.0
    # To make space for the fridge components in the shipping container
    FRIDGE_VOLUME_FT3 = 100

    @staticmethod
    def _make_bic_code(owner_code, serial):
        return iso6346.create(owner_code=owner_code,
                              serial=str(serial).zfill(6),
                              category='R')

    # The following two static methods convert from celsius to fahrenheit and from
    # fahrenheit to celsius.
    @staticmethod
    def _c_to_f(celsius):
        return celsius * 9/5 + 32

    @staticmethod
    def _f_to_c(fahrenheit):
        return (fahrenheit - 32) * 5/9

    def __init__(self, owner_code, length_ft, contents, celsius):
        """ Constructor """
        super().__init__(owner_code, length_ft, contents)

        if celsius > RefrigeratedShippingContainer.MAX_CELSIUS:
            raise ValueError("Temperature is too hot!")
        self.celsius = celsius

    # Use the '@property' decorator to make this method a property 'getter',
    # this will allow it to preform as if it were  an attribute.
    @property
    def celsius(self):
        return self._celsius

    # Use the function name WITH '<function>.setter' decorator to make this
    # method the property setter for the celsius attribute
    @celsius.setter
    def celsius(self, value):
        if value > RefrigeratedShippingContainer.MAX_CELSIUS:
            raise ValueError("Temperature is too hot!")
        self._celsius = value

    @property
    def fahrenheit(self):
        return RefrigeratedShippingContainer._c_to_f(self.celsius)

    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = RefrigeratedShippingContainer._f_to_c(value)

    @property
    def volume_ft3(self):
        # Call the property in the parent using 'super()' and then modify to shape
        # it to serve it's purpose in the derived class
        return super().volume_ft3 - RefrigeratedShippingContainer.FRIDGE_VOLUME_FT3

######################################################################################################


class HeatedRefrigeratedShippingContainer(RefrigeratedShippingContainer):

    MIN_CELSIUS = -20.0

    @RefrigeratedShippingContainer.celsius.setter
    def celsius(self, value):
        if value < HeatedRefrigeratedShippingContainer.MIN_CELSIUS:
            raise ValueError("Temperature is too cold!")
        RefrigeratedShippingContainer.celsius.fset(self, value)

