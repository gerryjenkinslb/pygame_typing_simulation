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

We have three python files:  `main.py`, `typing_area.py`, and `typing_area_sprite`.

The first defines a class called **TypingArea** that implements a rectangular are that can display
text onto. You can easily use this by creating a object and then calling the **update** and **draw** methods
main PyGame loop. Check out main.py for and example of using this class. 
The third file `typing_area_sprite` is a version of this that implements a PyGame DirtySprite object.

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
## DOCUMENTATION:

    FILE
        typing_area.py
    
    DESCRIPTION
        Class to support simulating human typing in an area
        in PyGame with Scrolling (known as typwriter effect)
        Inter-key timing is random based inspired by this paper:
           Dhakal, V., Feit, A., Kristensson, P.O. and Oulasvirta, A. 2018.
           'Observations on typing from 136 million keystrokes.'
           In Proceedings of the 36th ACM Conference on Human
           Factors in Computing Systems (CHI 2018). ACM Press.

    class TypingArea(builtins.object)
         TypingArea(text, area, font, fg_color, bk_color, wps=80)
         
         Class to automate a rectangular area that text is typed into in PyGame.
         A dirty sprite version: "TypingAreaSprite" is in file typing_area_sprite.py
         
         Use by creating object, call update and draw methods in the normal game loop
         
         Methods defined here:
         
         __init__(self, text, area, font, fg_color, bk_color, wps=80)
             Constructor: TypingClass(text, area, font, fg_color, bk_color, wps=80)
             
             Args:
                 text: text to display, add more using obj.text_buffer.extend(text)
                 area: PyGame Rect Object specifying the screen rectangle
                 font, fg_color, bk_color: font specs
                 wps: an optional parameter to set speed of typing, 80 wps default
         
         draw(self, screen)
             Call obj.draw() from the main game loop
         
         update(self)
             Call obj.update() from pygame main game loop

    
    FILE
        typing_area_sprite.py

    DESCRIPTION
        Constructor, draw(), and update() are same as TypingArea object, but
        this is a DirtySprite, see test code at bottom of file.

    CLASS
        TypingAreaSprite(pygame.Sprite.DirtySprite)
    
   

'''
