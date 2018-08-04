
# Animating Saturn with matplotlib, a subclass, and mock.patch()

_Based on my lightning talk at PyOhio 2018_

I hope that this comes across not as a complaint about matplotlib,
but as a celebration of tools that a dynamic language like Python
offers in situations where a library is seriously misbehaving
and needs some crucial live-edits to run successfully.

The task had seemed so simple.
To support an upcoming series of posts
based on my 2014 keynote at PyCon Ireland
(“Building the Medieval Universe in 7 Easy Steps with Scientific Python”),
I wanted to render an animation of one of the outer planets —
I chose Saturn —
progressing slowly eastward across the sky
over several seasons and several years.

<video autoplay loop height="648" width="648">
<source type="video/mp4" src="http://rhodesmill.org/brandon/2018/saturn.mp4">
</video>

Instead, I got to spend a weekend wrestling with matplotlib.

Once I had designed a static matplotlib figure
with Saturn drawn atop a field of glittering stars,
I was ready to try animating it.
Following the matplotlib documentation,
I instantiated an `Animation` object
and provided it with both the figure I had drawn
and a method that would update the position of Saturn for every frame.

    def update(frame_number):
        ...  # move Saturn

    anim = _Animation(fig, update)
    anim.to_html5_video()

The result was beautiful!
Saturn moves grandly across the sky,
swinging east and then west as our own planet’s orbit
carries our vantage point
first to one side of the Sun and then to the other.

But the animation rendered very slowly.
This little 96 kB movie somehow took several minutes to complete!

I wanted it to render more quickly —
not simply because I am impatient,
and not simply because I can make far more progress each hour
if I can iterate quickly on a design,
but because of a deep sense of proportion.
A modern computer can do a billion operations per second.
There is simply no reason that moving a circle in front of a star field
on a bitmap that’s only a few hundred pixels across
should take more than a few seconds.

And a solution was openly advertised
in [matplotlib’s own documentation](https://matplotlib.org/api/animation_api.html).
All I had to do was to get it to work.

## Asking for blitting

The mechanism for accelerating an animation
that features a static background is called “blitting,”
a venerable technique that has been a staple approach
since the early days of computer animation.
With this technique, the background is rendered first,
then each frame is constructed by making a copy of the static background bitmap
and painting the moving part of the animation on top.

Only two additional parameters are necessary
to activate blitting in matplotlib.

First, you add `blit=True`.

Second, Matplotlib needs two functions drawing functions instead of one:
the first returns the figure elements that belong to the background,
and the second does only the work of animation itself.

    def init(frame_number):
        ...  # return the star field

    def update(frame_number):
        ...  # move Saturn

    anim = _Animation(fig, update, blit=True, init_func=init)

The result, alas, was disappointing.

The rendering took exactly as long as before.

What was going wrong?
Why was matplotlib not behaving any differently?
To learn the answer,
I had to reach into my Python toolkit
and begin a dive into the innards of matplotlib.

## Festooning matplotlib with print()

Always remember
that a Python library installed with `pip` or `conda`
is simply a collection of files —
most of them plain-text Python source code —
owned by your user
and sitting somewhere beneath your home directory.

This means that you never need to treat a malfunctioning library
as a black box.
You can open its files in an editor,
find a routine whose behavior you want to understand,
and start adding all the `print()` calls you want
to learn what the routine is doing at runtime

Happily, the Jupiter notebook has an outstanding feature
that is a perfect match for this kind of work:

    %load_ext autoreload
    %autoreload 2

When you activate the “auto reload” extension,
IPython automatically detect edits to Python files and —
using some extraordinary inner magic of its own —
will make live updates to the functions and classes in your program
so that your edits take effect immediately.
You can see the result of editing and saving a source file
by simply re-running the notebook’s current cell.

It only took the barest of instrumentation
for me to find the first culprit:
`to_html5_video()` called the animation’s `save()` method
which makes an unfortunate decision about blitting:

    # TODO: See if turning off blit is really necessary
    anim._draw_next_frame(d, blit=False)

If I wanted the animation to render more quickly,
I would obviously have to convince matplotlib
that this `blit` parameter should instead be `True`.

## A subclass

Those who know me will appreciate my chagrin
when I had to admit to myself that, in this particular case,
a subclass really was the most natural means for defeating
the `save()` method’s unfortunate behavior.

So I wrote a subclass.

For a moment I thought that the solution
would be a subclass of `Animation`
that overrode the `save()` method itself —
after all, it was `save()` that was setting `blit` incorrectly.

But as soon as my cursor was poised inside of the new subclass,
I saw that overriding `save()` would be the wrong approach.
In order to tweak that one line of code,
I would have to cut and paste the entire method —
which weighs in at 99 lines of code!
In general,
you want to avoid repeating any code from the parent class
when constructing its child.

Instead, the solution was to leave `save()` broken
but override the method it was calling
to ignore the parameter’s value.

    class _Animation(FuncAnimation):
        def _draw_next_frame(self, framedata, blit):
            blit = True
            super(_Animation, self)._draw_next_frame(framedata, blit)

Then I asked matplotlib to re-render my animation.
The result?

It now rendered in half the time.

## And you thought mock.patch() was for tests

But, wait — _half_ the time?
Something was obviously wrong.

Eliminating the star field rendering from every frame
should have sped up the animation by a factor of a hundred,
not merely by a factor of two.
What extra work was matplotlib doing
that was as expensive as the star field render I had just eliminated?

It was time to add more `print()` calls.

It was at this point
that `autoreload` started to run into trouble.
I would add `print()` calls but they wouldn't print.
I would edit files, but the edits would have no effect.
Only when I restarted the notebook kernel
would I receive output and see the effects of new code

How was matplotlib defeating
the clever techniques built in to `autoreload` in IPython?

The answer is that matplotlib was using
even more nefarious techniques of its own —
techniques that were also defeating my own ability to simply read its code.
After repeatedly seeing methods invoked at runtime
that I could not find on the same class in the source code,
I finally discovered this:

    @functools.lru_cache(None)
    def subplot_class_factory(axes_class=None):
        # This makes a new class that inherits from SubplotBase and the
        # given axes_class (which is assumed to be a subclass of Axes).
        # This is perhaps a little bit roundabout to make a new class on
        # the fly like this, but it means that a new Subplot class does
        # not have to be created for every type of Axes.
        if axes_class is None:
            axes_class = Axes
        return type("%sSubplot" % axes_class.__name__,
                    (SubplotBase, axes_class),
                    {'_axes_class': axes_class})

Alas!

It turns out that matplotlib generates classes at runtime.
And constructs them by combining regular classes with mix-ins.
And it even stores them in a little dynamic class cache for use later.

It was, predictably, these dynamically-generated classes
which were not getting reloaded by IPython
when I would edit their source code;
`autoreload` had met its match.

Once I stopped relying on `autoreload` and got moving again,
the terrible truth was revealed.
The reason that blitting had only eliminated half my rendering time
was because matplotlib was rendering every frame twice.
Its technique for producing a frame of the animation, in other words, was:

* Make a copy of the star field background
* Draw Saturn in the correct position for this frame on top
* Throw the resulting image away
* Start over with a new image
* Draw the star field
* And draw Saturn

But, why?
What method call was launching a redundant and expensive re-rendering
of the entire figure?

It's easy in Python to discover why something is called the first time.
Simply toss an error into its source code
(I normally just open a new line and type `asdf`)
and run your program.
A traceback will appear showing you the site of the function’s
very first invocation.
But to get a traceback for a second or third invocation,
your booby trap needs to be a little more elaborate.
I usually use a variation on:

    BCR = []  # mutable global at the top of the file

    # Then, inside the function or method:
        if BCR:
            asdf
        BCR.append(None)

The resulting traceback showed me exactly what I needed to know!

* After `Animation.save()` calls `Animation._draw_next_frame()`
  to render the frame to its bitmap canvas,
  it invokes `FileMovieWriter.grab_frame(...)`
  to add the frame to the growing animation.

* Presumably needing a copy of the completed bitmap,
  `grab_frame()` calls `Figure.savefig(...)` on the diagram.

* But `savefig()` prefers to delegate the actual act of drawing
  to other classes.
  After making sure that a whole list of defaults have been properly set,
  it calls its canvas’s `print_figure(...)` method.

* Which is a method that lives over on the class `FigureCanvasBase`,
  a method with a reassuringly concrete docstring description:
  “Render the figure to hardcopy.”
  Confusingly, while `savefig()` thought of this object
  itself as the figure’s “canvas,”
  here in `print_figure()` what we might call the “real canvas”
  is revealed to be an object yet deeper in the hierarchy
  which is acquired by learning the requested output format,
  building the string `'print_%s' % format`,
  and using `getattr()` to get that method from the canvas.
  In our case the method fetched is named `'print_raw'`.

* Which winds up invoking a method `print_raw()` in `FigureCanvasAgg`,
  a subclass of the `FigureCanvasBase` we were just discussing.
  Subtracting out a bit of preparation involving DPI,
  `print_raw()` mostly exists to send `fileobj.write()`
  the data from a call to `self.get_renderer()._renderer.buffer_rgba()`.
  Which sounds more or less like what we would hope it would be doing:
  rendering an RGBA bitmap.
  Except that, _before_ using the renderer to save data to the file,
  `print_raw()` — apparently in a momentary loss of confidence
  that there’s even data ready to save —
  calls `FigureCanvasAgg.draw()` on itself
  and winds up drawing the entire frame over again.

So there we are.
I saw that if I could simply disable the method `FigureCanvasAgg.draw()`,
I could skip the re-rendering and animate at full speed!

But in this case,
I couldn't simply build a subclass to skip the animation,
because I wasn't the one who even instantiated
whatever subclass of `FigureCanvasAgg` was involved here.
While I could have reached into the maze of live matplotlib objects
and attempted to edit the object in-place,
I usually find it faster to attack the class instead.
I reached into the Python toolbox
for everybody's favorite tool for subverting production code:
`mock.patch()`.

    DRAW = 'matplotlib.backends.backend_agg.FigureCanvasAgg.draw'

    def no_nothing(self):
        pass

    with patch(DRAW, do_nothing):
        anim.to_html5_video()

The first run of my animation with this improvement in place
ran at blazing speed!

## Pulling mock.patch() to pieces

There was only one problem.

The star field was now entirely missing.
Saturn was pacing back and forth, lonely,
across an empty sky of solitude.

I realized that I needed to let `FigureCanvasAgg.draw()`
run once at the beginning,
to render the star field,
before I turned it off for the rest of the animation.
Happily, Python exposes the innards of its context managers like `mock.patch()`
which makes it possible to call them in phases:

    class _Animation(FuncAnimation):
        patcher = None

        def _draw_next_frame(self, framedata, blit):
            blit = True
            super(_Animation, self)._draw_next_frame(framedata, blit)
            if self.patcher is None:
                self.patcher = patch('matplotlib.backends.backend_agg'
                                     '.FigureCanvasAgg.draw', do_nothing)
                self.patcher.__enter__()

        def save(self, **args, **kw):
            super(_Animation, self).save(**args, **kw)
            self.patcher.__exit__()

By not entering `mock.patch()` until the animation has drawn the background
and called `_draw_next_frame()` for the first time,
I leave the `draw()` method alive
during the crucial step of rendering the star field.
Note that I’m also careful to exit the patch
when I’m done with it at the very end —
if you forget that, it turns out,
then all future animations will also be missing their background!

With these careful adjustments in place,
the animation worked perfectly,
and ran with blazing speed.
I was now unblocked
and free to move forward with my animation work.

Oh — and, all those `print()` calls that now festooned matplotlib?
I advise against trying to remove them one by one.
You’ll think that you have them all removed,
but months later random debugging output will appear
in the middle of an IPython notebook when you least expect it.
If by that point you forgot about even adding them,
it might take a bit of work
before you realize where the output is coming from.

So don't try to remove them manually.
Uninstall the package, reinstall the package, and then restart IPython.
It’s the only way to be sure.
