# A Descriptor-Constructor in Python

<!-- Date: 2022 January 26 -->

So here’s an API innovation that I just made a rough implementation of:
taking a Python data descriptor and enhancing it so that,
when it’s invoked on the class itself,
it becomes a constructor and returns a new instance of the class.

Does that sound like a good idea?

After you’ve read the saga below,
feel free to share your opinion
by replying to my tweet about this post!

<https://twitter.com/brandon_rhodes/status/1486435857607311368>

The background is that my astronomy library Skyfield
uses objects to represent measures like distance and velocity.
I could have used two separate objects
to represent a distance measured as `au` (astronomical units)
and a distance measured as `km`,
but I prefer not to have several objects represent one single thing.
It seems cleaner to me to have but a single object
for each particular distance that Skyfield needs to represent,
and to have that object different offer units
as different attributes
(which also helps readability
by making users name the unit they’re asking the `Distance` for):

<!--phmdoctest-share-names-->

```python
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
```

```
au: 1.4505554055322529e-06
km: 217.00000000000003
```

At least that’s how I implemented it back in 2014.
In retrospect I’m not happy with how `__init__()` works.
To my eyes today it looks wasteful:
only one of the several arguments is ever used,
and the `if…elif` has to search through them every time,
even though only one will ever be non-`None`.

Side note —
I felt so bad about this `__init__()` code
that Skyfield’s `Distance` class
provides a second, redundant constructor for `au`:

```python
    @classmethod
    def from_au(cls, au):
        self = cls.__new__(cls)  # avoid calling __init__()
        self.au = au
        return self
```

You’ll recognize this pivot as a
[modern design pattern that I discuss on my Python Patterns site](https://python-patterns.guide/gang-of-four/composition-over-inheritance/#dodge-if-statements):
instead of providing one huge method
with a big `if…elif` inside that decides what it should do,
simply have *n* smaller methods
that each do one thing well.

Anyway.

Another problem with the example code above
is that `.km` needs to be computed over and over again
every time the user needs it.
In a loop, that could become expensive:
a Skyfield distance isn’t always a simple float,
it can be a whole NumPy array of a million elements.

At first I avoided recomputing it
by using one of those unwieldy `if self._km is None:`
caching checks inside of each unit’s property,
but then I remembered that Python descriptors
were very carefully designed
so that you could write a descriptor
that only gets called if there isn’t yet a `.km` attribute!
Otherwise Python skips the whole method call,
which both makes the logic simpler and saves valuable time.
I never remember the formula,
so I had to look it up (I got it from Pyramid’s source code):

<!--phmdoctest-share-names-->

```python
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
```

I never quite remember what all its code is doing,
but it works great!

<!--phmdoctest-share-names-->

```python
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
```

```
au: 1.524
km: 227987154.9468

au: 1.4505554055322529e-06
km: 217
```

When we use `@reify` to turn `.km` into a real attribute like this,
that we can assign to,
we get an extra benefit:
when a distance is instantiated using `km`,
we can cache the actual value that the user provided!
Note that we are now returning the exact `km` value the user provided,
instead of trying to re-convert the value from `au`
and getting the slight rounding error we saw in the first example:
`km` is now `217` instead of `217.00000000000003`.

But how can we avoid the ugly `if…elif` block,
and the need to have `__init__()` accept as many parameters
as there are units of measurement?

I already illustrated, above,
a `from_au()` method that does things the ‘right way’
by multiplexing on method name rather than on combinations of arguments.
Is that the way forward,
adding something like `from_km()`
for each additional unit supported?
That way forward still seems a little sad:
if I need to support _n_ units,
then I need to write _n_ constructors in addition to my _n_ reified properties,
and keep them all in sync with each other.

Could there be a better way?

Like a sudden blaze of light, a possible constructor syntax occurred to me:

```
d = Distance.km(217)
```

Wow!
Could it work?
Could a `@reify` descriptor
be taught to respond to a class-method-like call
and return a newly constructed instance?
What even happens when that syntax is invoked?

```python
try:
    Distance.km(217)
except Exception as e:
    print(e)
```

```
'reify' object is not callable
```

A bit of testing revealed
that calling the `reify` descriptor like a function
does something very Pythonic and obvious:
it runs its `__call__()` method if it has one.
Simple enough!
Let’s write a better `reify`:

<!--phmdoctest-share-names-->

```python
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
```

```
type(self): <class 'tmp.test_code_214_output_243.<locals>.unit'>
args: (217,)
```

It worked!
Our new extended descriptor is starting to gain a superpower
beyond what `@reify` itself could do:
it supports being called like a method of the class itself.
Can we turn it into a constructor?

Well, let’s see what else the constructor will need.

It will need to know the name of the attribute to set
on the new instance.
That’s easy enough: it can ask for the `__name__` of the method,
and it will learn that it’s named `km`.
What about learning the conversation factor that it needs to use?
We don’t currently have a way to provide it.
Maybe the decorator should take an argument —
which is conventionally accomplished in Python
by turning the decorator into a closure that returns an inner function.

Oh, dear, this is going to be a bit ugly, isn’t it?
Let’s just get it working and maybe we can simplify later.

<!--phmdoctest-share-names-->

```python
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
```

```
name: km
conversion_factor: 149597870.7
value: 217
```

Success!
The `__call__()` now knows what attribute it should set
and what conversion factor it should apply.
Yes, I dislike creating classes inside of functions inside of other functions.
But let’s see if we can get it working before we worry about elegance.
It feels like time to write up some actual constructor code
and see if we can get a `Distance` instance returned back to us.

Well — drat.

How will `__call__()` know what class to build?

I could of course hard-code `Distance` as the class to build,
but I was hoping that a single descriptor
could support all of my classes,
including `Velocity` and `Angle`.
It would be better if `unit` could auto-discover
that `Distance` was the class it was being asked to build.
But, alas, it doesn’t know its class!
Remember that the `self` argument to `__call__()`,
as you might have noticed in the earlier example,
is the `unit` descriptor instance itself —
which makes sense,
but doesn’t help me discover
which class this `unit` descriptor is attached to.

And here we run into a quirk of Python:
methods don’t know which class they belong to.
And decorators don’t have a way to get to the class either —
the class object doesn’t even exist yet
as the class’s namespace itself is running.

One common solution is to do post-processing on the class.
Then you can loop over its attributes,
figure out which ones are `unit` descriptors,
and give them each an extra attribute, like `_my_class`,
that tells them what class they belong to.

There are several well-known ways to post-process a Python class.

* We could pass the class to a simple function.
* We could use a class decorator (available since Python 2.6).
* We could go all unreadable-old-school and use a metaclass.

But then there would be a subtle problem.
Though it would probably never come up,
it’s technically incorrect for `km()` to always return a `Distance`,
because someone could subclass `Distance`
and then the `km()` constructor, if called on their subclass,
really ought to return an instance of that subclass instead.

And — those approaches just feel *complicated*
compared to what we’re trying to do.
Is it really impossible for `__call__()` to learn its class?

So I dug around a bit.
I added `print()` statements in a variety of places.

And discovered a solution!

To my vast surprise,
it turns out that the method call:

```
Distance.km()
```

— goes through, not one, but _two_ of the methods
defined on the `unit_descriptor`!
The steps Python take turn out to be:

1. `Distance` — look up the object.
2. `.km` — Grab the `km` attribute.
3. Oh, wait! It’s a descriptor! So Python auto-invokes
   `__get__(None, Distance)`
   and the resulting object is considered
   the actual value of the attribute.
4. `()` — Finally, Python invokes that object’s `__call__()` method.

And while the knowledge ‘which class was this called on’ has evaporated
by the time `__call__()` is invoked,
_it’s available inside the ‘get’ dunder!_

Recall that at this point we’re using a `__get__()` method
that I copied-and-pasted from the Internet
without actually understanding what it does.
Let’s look at it again —
this time, pay attention to its first two lines:

```
            def __get__(self, instance, objtype=None):
                if instance is None:
                    return self
                value = self.method(instance)
                instance.__dict__[self.__name__] = value
                return value
```

Yeah, I didn’t understand them at first either.
Why would `instance` be `None`?
Well, it turns out, that’s what tells the descriptor that you,
instead of asking for an instance attribute `d.km`,
have asked for a class attribute `Distance.km`.
And it just so happens that in that case,
`objtype` is `Distance`!

So we can get rid of `__call__()` entirely!
We didn’t know it,
but it turns out that we were already intercepting
the `Distance.km()` class method —
we just weren’t doing anything interesting yet.
Let’s fix that:

```python
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
```

```
au: 1.4505554055322529e-06
km: 217
```

Amazing! It works!

To avoid having to tell `constructor()` too many new facts,
we go ahead and embed it inside the closure
so that it can get values like `conversion_factor` and `core_unit`
for free.
The only thing it’s missing is the class it’s supposed to build,
whether that’s `Distance` or `Velocity`,
but we can provide that easily enough using a partial —
creating, in essence, a little hand-made bound method
that already knows its first argument.

(Yes, I could have instead used some black magic from Stack Overflow
to create a real bound method.
No, I am not in the least tempted to do so.)

The mission is now accomplished!

But code is kind of ugly:
we’re building an inner class, inside of a function,
inside of another function.

A final simplification fell out
when I noticed that we were having to state twice,
redundantly,
the name of the unit and how to perform its conversion.
Remember that the method we’re decorating still looks like this:

```
    @unit(AU_KM, 'au')
    def km(self):
        return self.au * AU_KM
```

Why mention `au` and `AU_KM` twice?
That’s the kind of thing a descriptor is supposed to take care of for us!
So let’s abandon the complexity of wrapping a method,
abandon the need to have a closure,
and refactor back to a plain descriptor:

```python
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
```

```
au: 1.524
km: 227987154.9468

au: 1.4505554055322529e-06
km: 217
```

Well.
What do you think?

Will I regret this later if I push this to production?

Again, replies to
[my tweet](https://twitter.com/brandon_rhodes/status/1486435857607311368)
are welcome!
