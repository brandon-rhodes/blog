"""pytest file built from texts/brandon/2022/a-descriptor-constructor.md"""
import pytest

from phmdoctest.fixture import managenamespace
from phmdoctest.functions import _phm_compare_exact


def test_code_33_output_52(capsys, managenamespace):
    AU_KM = 149597870.700

    class Distance:
        def __init__(self, au=None, km=None):
            if au is not None:
                self.au = au
            elif km is not None:
                self.au = km / AU_KM

        @property
        def km(self):
            return self.au * AU_KM

    d = Distance(km=217)
    print('au:', d.au)
    print('km:', d.km)

    _phm_expected_str = """\
au: 1.4505554055322529e-06
km: 217.00000000000003
"""
    _phm_compare_exact(a=_phm_expected_str, b=capsys.readouterr().out)
    managenamespace(operation="update", additions=locals())


def test_code_69():
        @classmethod
        def from_au(cls, au):
            self = cls.__new__(cls)  # avoid calling __init__()
            self.au = au
            return self

    # Caution- no assertions.


def test_code_106(managenamespace):
    from functools import update_wrapper

    class reify(object):
        def __init__(self, method):
            self.method = method
            update_wrapper(self, method)

        def __get__(self, instance, objtype=None):
            if instance is None:
                return self
            value = self.method(instance)
            instance.__dict__[self.__name__] = value
            return value

    # Caution- no assertions.
    managenamespace(operation="update", additions=locals())


def test_code_127_output_149(capsys, managenamespace):
    class Distance:
        def __init__(self, au=None, km=None):
            if au is not None:
                self.au = au
            elif km is not None:
                self.km = km
                self.au = km / AU_KM

        @reify
        def km(self):
            return self.au * AU_KM

    d = Distance(au=1.524)
    print('au:', d.au)
    print('km:', d.km)
    print()
    d = Distance(km=217)
    print('au:', d.au)
    print('km:', d.km)

    _phm_expected_str = """\
au: 1.524
km: 227987154.9468

au: 1.4505554055322529e-06
km: 217
"""
    _phm_compare_exact(a=_phm_expected_str, b=capsys.readouterr().out)
    managenamespace(operation="update", additions=locals())


def test_code_194_output_201(capsys):
    try:
        Distance.km(217)
    except Exception as e:
        print(e)

    _phm_expected_str = """\
'reify' object is not callable
"""
    _phm_compare_exact(a=_phm_expected_str, b=capsys.readouterr().out)


def test_code_214_output_243(capsys, managenamespace):
    class unit(object):
        def __init__(self, method):
            self.method = method
            update_wrapper(self, method)

        def __get__(self, instance, objtype=None):
            if instance is None:
                return self
            value = self.method(instance)
            instance.__dict__[self.__name__] = value
            return value

        # New code:

        def __call__(self, *args):
            print('type(self):', type(self))
            print('args:', args)


    class Distance:
        # ...
        @unit
        def km(self):
            return self.au * AU_KM

    Distance.km(217)

    _phm_expected_str = """\
type(self): <class 'tmp.test_code_214_output_243.<locals>.unit'>
args: (217,)
"""
    _phm_compare_exact(a=_phm_expected_str, b=capsys.readouterr().out)
    managenamespace(operation="update", additions=locals())


def test_code_271_output_309(capsys, managenamespace):
    def unit(conversion_factor):
        def wrap(method):
            name = method.__name__

            class unit_descriptor(object):
                # These methods are the same as before:

                def __init__(self, method):
                    self.method = method
                    update_wrapper(self, method)

                def __get__(self, instance, objtype=None):
                    if instance is None:
                        return self
                    value = self.method(instance)
                    instance.__dict__[self.__name__] = value
                    return value

                # This is improved:

                def __call__(self, value):
                    print('name:', name)
                    print('conversion_factor:', conversion_factor)
                    print('value:', value)

            return unit_descriptor(method)
        return wrap

    class Distance:
        # ...
        @unit(AU_KM)
        def km(self):
            return self.au * AU_KM

    Distance.km(217)

    _phm_expected_str = """\
name: km
conversion_factor: 149597870.7
value: 217
"""
    _phm_compare_exact(a=_phm_expected_str, b=capsys.readouterr().out)
    managenamespace(operation="update", additions=locals())


def test_code_428_output_471(capsys):
    from functools import partial

    def unit(conversion_factor, core_unit):
        def wrap(method):
            name = method.__name__

            class unit_descriptor(object):
                def __init__(self, method): # Same as before
                    self.method = method
                    update_wrapper(self, method)

                def __get__(self, instance, objtype=None):
                    if instance is None:    # New behavior:
                        return partial(constructor, objtype)
                    value = self.method(instance)
                    instance.__dict__[self.__name__] = value
                    return value

            # New way to build a Distance:

            def constructor(cls, value):
                obj = cls.__new__(cls)      # Make a new Distance
                setattr(obj, name, value)   # “Set .km to 217”
                if conversion_factor is not None:  # And set “.au”
                    value = value / conversion_factor
                    setattr(obj, core_unit, value)
                return obj

            return unit_descriptor(method)
        return wrap

    class Distance:
        # ...
        @unit(AU_KM, 'au')
        def km(self):
            return self.au * AU_KM

    d = Distance.km(217)
    print('au:', d.au)
    print('km:', d.km)

    _phm_expected_str = """\
au: 1.4505554055322529e-06
km: 217
"""
    _phm_compare_exact(a=_phm_expected_str, b=capsys.readouterr().out)


def test_code_516_output_552(capsys):
    class unit(object):
        def __init__(self, name, conversion_factor=None, core_unit=None):
            self.name = name
            self.conversion_factor = conversion_factor
            self.core_unit = core_unit

        def __get__(self, instance, objtype=None):
            if instance is None:  # If called as a class method:
                def constructor(value):  # (same as above)
                    obj = objtype.__new__(objtype)
                    setattr(obj, self.name, value)
                    conversion_factor = self.conversion_factor
                    if conversion_factor is not None:
                        value = value / conversion_factor
                        setattr(obj, self.core_unit, value)
                    return obj
                return constructor
            value = getattr(instance, self.core_unit)
            value = value * self.conversion_factor
            instance.__dict__[self.name] = value
            return value

    class Distance:
        au = unit('au')
        km = unit('km', AU_KM, 'au')

    d = Distance.au(1.524)
    print('au:', d.au)
    print('km:', d.km)
    print()
    d = Distance.km(217)
    print('au:', d.au)
    print('km:', d.km)

    _phm_expected_str = """\
au: 1.524
km: 227987154.9468

au: 1.4505554055322529e-06
km: 217
"""
    _phm_compare_exact(a=_phm_expected_str, b=capsys.readouterr().out)
