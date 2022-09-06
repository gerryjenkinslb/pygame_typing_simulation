## PyGame Typewriter Effect to Simulate Human Typing

related video: [PyGame human typing](https://youtu.be/4njHgre-pKM)

A viewer of my [YouTube video on how to use PyGame dirty Sprites](https://youtu.be/Pu5_8F_KaHI) 
asked how to create a PyGame Sprite that would simulate a human typing text.

So I though I would work on that. First I needed to work out how to just display text in a dynamic way that 
would look like a user was typing inside a rectangular surface and start to scroll up when they got to the bottom.
You can see how I did this in my video
[PyGame: Scroll Text - Technique and Code Walk Through](https://youtu.be/PWd2CJfdx1A)


https://user-images.githubusercontent.com/905148/171503515-b38d1bdf-5e4a-43f8-90f6-15dffe5c23ce.mp4


----
## PyGame_typing_simulation Code base

We have two files:  `main.py` and `typing_area.py`.

The first defines a class called **TypingArea** that implements a rectangular are that can display
text onto. You can easily use this by creating a object and then calling the update and draw methods
main PyGame loop. Check out main.py for how to call it.

`typing_area.py`:
In the code we need to handle the timing in pygame
and when to advance a line or to scroll up if we have reached the end of the area
we also handle of course the char by char display to simulate typing. I hope the
comments are a good guide as to what is happening.

> *I will be working on an article and video for a code walk-through soon.*
>
>-- enjoy, \
>   &nbsp;&nbsp;&nbsp;**Gerry Jenkins**
> 
> 
---
# DOCUMENTATION:

## TypingArea Objects

```python
class TypingArea()
```

Class to automate a rectangular area that text is typed into in PyGame. You can easily covert this
class to a Sprite if needed

To use, just create object, and call the update and draw methods in the normal game loop

**Arguments**:

- `file_loc` _str_ - The file location of the spreadsheet
- `print_cols` _bool_ - A flag used to print the columns to the console
  (default is False)

#### \_\_init\_\_

```python
def __init__(text, area, font, fg_color, bk_color, word_per_min=80)
```

Constructor call  TypingClass(text, area, fond, fg_color, bk_color, word_per_min=80)

**Arguments**:

- `text` - string of test to display, can add more by using obj.text_buffer.extend(text)
- `area` - PyGame Rect Object specifying the screen rectangle
  font, fg_color, bk_color: font and its foreground and background color
- `word_per_min` - an optional parameter to set speed of typing

#### update

```python
def update()
```
