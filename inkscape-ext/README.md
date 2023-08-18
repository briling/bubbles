# Bubble bond Inkscape extension

This is an [`inkscape`](https://inkscape.org/) extension 
that uses the [`bubbles`](../) library
to draw bonds between bubbles.

## Requirements (under construction)

Should work with `python3` and `inkscape>=1` (I have `python3.6` and `inkscape 1.0.1`).

## Installation

Install the main `bubbles` package and put/link
`bubblebond.py` and `bubblebond.inx`
in `~/.config/inkscape/extensions/`
(or the directory listed at `Edit > Preferences > System: User extensions`).

It should be possible to avoid installing the main package by copying the main
`bubbles/bubbles.py` file into this directory (the one linked/copied in inkscape's
extensions directory)

## Usage

Select two bubbles you want to bond 
and go to `Extensions > Bubble bond`. 

![screencast](screencast.gif)
