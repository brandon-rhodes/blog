---
categories: Computing
date: 2012/06/14 23:58:03
permalink: http://rhodesmill.org/brandon/2012/quietly-pushing-to-heroku/
title: Throwaway Commits on Heroku
---

`As Ian Bicking himself once observed <http://blog.ianbicking.org/2012/02/14/git-as-sync-not-source-control-as-deployment/>`_,
the process of deploying an application to Heroku
can be quite costly when measured in commits.
Your Git history can become littered with dozens of tiny changes
as you adjust your application
so that everything —
your database, authenticated memcache, remote logs —
finally starts to function smoothly inside of the Heroku sandbox.

The Heroku deployment process itself can be quite valuable.
Just like the discipline of writing tests
tends to reveal whether code is tightly coupled,
your first deploy to Heroku can reveal all sorts of ways
in which you were relying on a persistent filesystem
without quite admitting it to yourself.
Sure, you knew that *in theory* an EC2 instance
could disappear at any moment,
but not until moving to a scorched-earth form of deployment —
that wipes out temporary files on every code update —
are you really forced to face the question
of whether your application can periodically wake up in a fresh sandbox
without skipping a beat.

But, as Ian says, Heroku deployment can lead
to a dozen successive commits that all say
“another try at parsing the database URL correctly”
because the only way to test your one-character change
is to commit and push.

Forgetting
----------

Perusal of the Git documentation convinced me
that there was a way around the Heroku version-control dilemma.
Because Git is a rowdy steampunk agglomeration of switches and levers,
and not a clean and elegant permanent history fortress like Mercurial,
it offers all sorts of convenient ways
to quickly destroy inconvenient history.

* By doing a ``reset`` ``--soft``
  you can safely discard a few recent commits,
  leaving the actual changes that you made
  still applied to the files that you have been editing.

* Making a remote repository forget all of the commits
  that you have obliterated from your local repository
  is as easy as doing a ``push`` with the ``--force`` flag.

My first experiment —
which of course I inflicted on the development instance of my app,
not the Heroku app that runs it in production! —
went something like this::

  #!bash
  # Messy first experiment

  $ git ci . -m 'adjusted database parameters'
  $ git push heroku master

  # Did some editing

  $ git ci . -m 'more adjusting'
  $ git push heroku master

  # Did some more editing

  $ git ci . -m 'even more adjusting'
  $ git push heroku master

  # The deploy finally worked!
  # Time to back out all three commits

  $ git reset --soft HEAD~3
  $ git push heroku master --force

Now I am back where I had started,
as if none of the three commits has ever happened.
More importantly, my repository on Heroku is also rewound
so that Git will not become confused
the next time I try to push.

A quick ``git`` ``diff`` confirms that the changes
I was experimenting with are still present on my filesystem.
I can now make a single “good” commit of a complete solution,
instead of having to preserve every misstep along the way.

Automating the throwaway commit
-------------------------------

But, of course, it is dangerous
to construct an expression like ``HEAD~3``
and hope that I have correctly counted back to the most
recent commit that I want to keep.

So I will recommend two safeguards.
First, never let your repository get more than one commit
ahead of the “real” most recent version.
Second, use a simple shell script to automate your Heroku
configuration trials so that you minimize the chance of human error.
For example, you might try::

  #!bash
  #!/bin/bash
  # try-it-on-heroku.sh
  # Temporarily test our current edits on Heroku

  set -e

  git ci . -m 'Heroku temporary commit'
  git push heroku master --force

  echo
  echo "Press Enter once you have tested the app on Heroku"
  read

  git reset --soft HEAD~1
  git push heroku master --force

  echo
  echo "Okay, the app is restored to where it was before"
  echo

I can run this script over and over again
without advancing my true version history by a single commit,
gradually honing in on the correct parameters and syntax
for talking to crazy Heroku SSL-authenticated memcache (or whatever).
Once it works, I do the real commit by hand
and push the result up to GitHub as a keeper.

Note that, as a matter of routine, I add ``--force`` to every
Heroku push in my shell scripts.
This is because I never use Heroku to store my repository of record,
since repositories there disappear as soon as I need to delete
a particular app and start over again.
Since I consider the Git history on Heroku to be throwaway —
unlike the history on my disk and at GitHub —
I have no qualms about always forcing Heroku's copy
to update itself to exactly what I have on my laptop.

Bonus round: deploying generated files
--------------------------------------

Heroku's use of Git as its deployment mechanism
presents another dilemma:
how do you handle files
that do not need to be kept under version control —
they are simply derived from other files in your repository —
but that are difficult to build in the Heroku sandbox?
Three separate issues are involved.

1. Repositories are unhappy places for many of the generated files
   that we create for production deployment.
   Exhibit A would, of course,
   be compressed and minified JavaScript and CSS.
   Minified code often looks like a huge single line that changes,
   *in its entirety*, every time you tweak your code at all.
   Git will not be amused.

2. But the Heroku sandbox can be an unhappy place
   for running last-minute build steps like minification.
   For one thing,
   it can be unclear how you would even launch your minify script
   in time for its output to be included in the Heroku slug.
   For another,
   you might have to create your own Build Pack full of tools.
   Your Heroku sandbox probably does not include
   things like the Closure Compiler, the Compass framework,
   or UglifyJS by default.

3. Generated files can be quite large,
   and small changes to your source code
   can produce hundreds of lines of difference in generated output
   when you are adjusting, say, the master template of a static site.
   If you multiply this effect by hundreds of commits
   over the lifetime of a project,
   then your repository can start approaching a size
   near the limits of what Heroku will accept.

Happily, there is an easy solution.
We use the discussion above
as a guide for making a temporary commit to Heroku,
but this time we *leave the commit there*
as our final running production version of the app.

Of course, I automate the process with a shell script.
The details will vary with project,
but a deploy script might look roughly like this::

  #!bash
  #!/bin/bash
  # project/bin/deploy.sh
  # Build everything and deploy this app to Heroku

  set -e

  # Change to the project root directory

  cd "$(dirname ${BASH_SOURCE[0]})"
  cd ..

  # Build

  bin/compass compile
  bin/uglifyjs scripts/app.js > scripts/app.min.js

  # Temporarily add the generated files to version control
  # (-f says "even though this file is in .gitignore")

  git add -f styles/app.css
  git add -f scripts/app.min.js

  # Push them to Heroku, then repent of the commit

  git ci . -m 'Temporary Heroku-only deployment commit'
  git push heroku master --force
  git reset --soft HEAD~1

  # Un-stage the generated files to finish

  git reset HEAD -f styles/app.css
  git reset HEAD -f scripts/app.min.js

This can be especially fun
if you are using the
`Static Sites on Heroku Cedar <http://kennethreitz.com/static-sites-on-heroku-cedar.html>`_
methodology pioneered by Kenneth Reitz.
Your site will be completely static,
with no code running at all in production,
so an approach like this is your only chance to throw
in generated content as you deploy.

This last shell script does not play well
with other changes that you might have left sitting around
in your working directory — your ``git`` ``st`` output
should be clean before you set the script in motion.

Please note that history-altering strategies like this
can be dangerous, and should only be undertaken if you
thoroughly understand the Git commands that are involved.
Do experiments with a temporary checkout of your project
before convincing yourself that this methodology will work
with your own particular application and Heroku account.
But if these strategies work for you,
then they should remove some of the pain
of using a version control system to do deployment!
