# -*- coding: utf-8 -*-
"""
Type Speed Test App

Created on Fri Jan  7 12:41:22 2022

@author: ANAT-H
"""
import tkinter as tk
from random import choice
from text_samples import samples
from timeit import default_timer as timer
import string
from PIL import ImageTk, Image


BACKGROUND_COLOR = "#516BEB"
TITLE_FONT = ("Cabin Sketch Regular", 30, "bold")
SUBTITLE_FONT = ("Cabin Sketch Regular", 22, "bold")
BUTTON_FONT = ("Arial",13, "normal")
FONT = ("Corbel",20, "normal")
RESULT_FONT = ("Cabin Sketch Regular", 25, "bold")
LETTERS = string.ascii_lowercase + string.ascii_uppercase 
AVG_WPM = 40

def refresh_text():
    '''
    Picks a new random sample text from samples
    '''
    global start, sample_text, result_image
    
    # Sets text box active
    text_box.config(state="normal", bg='#fff')
    
    # Presents new sample text and removes image if necessary
    result_image.grid_forget()
    sample_text = choice(samples)
    text.config(text=f'{sample_text}', fg ='#EDD2F3', font=FONT)
    text.grid(column=0, columnspan=2, pady=0)
    
    # clears text box & resets start time
    text_box.delete('1.0',tk.END) 
    start = 0

def timing(event):
    '''
    Calculates words-per-minute typed by the user.
    Timing starts at first letter key stroke and stops at Enter key stroke.
    
    Parameters
    ----------
    event : tkinter.Event
        The key pressed by the user.

    '''
    global start, high_score
    
    # Starts timing at first letter typed.
    if event.keysym in LETTERS and start == 0.0: 
        start = timer()  
   
    # Stops timing at Enter  & reset start time.
    elif event.keysym == 'Return':
        time = timer() - start
        start=0
    
        # Get user input & disable text box 
        user_input = text_box.get("1.0", tk.END)
        text_box.config(state="disabled", bg='#c8c8c8')  
        
        sample_words = sample_text.split()
        n_sample_words = len(sample_words)
        input_words = user_input.split()
        
        # Check that there are enough words typed in
        if len(input_words) < n_sample_words/2:
            text.config(text='Not enough words typed,\nrefresh and try again...',
            fg='#84DFFF',  font=RESULT_FONT)
            text.grid(pady=30)  
            return

        # Calculate how many correct words were typed.
        n_correct = 0
        for word in input_words:
            if word in sample_words:
                n_correct += 1
                sample_words.remove(word)  
                  
    
        # Calculate words-per-minute, present results.
        words_per_min = round(60*(n_correct/time))
        
        if  words_per_min >= high_score:
            high_score = words_per_min
            with open('high_score.txt', 'w') as score:
                    score.write(f'{high_score}')
            high_score_label.config(text=f'High Score: {high_score} WPM')        

        # Display image
        if words_per_min >= AVG_WPM:
            image = Image.open("PngItem_thumbs-up.png")
            to_avg = 'Equal/Above average'
                      
        else:
            image = Image.open("pngfind.com-thumbs-down.png")
            to_avg = 'Below average'
        
        text.config(text=f'Your result is: {words_per_min} WPM\n{n_correct} ' 
                    f'correct words out of {n_sample_words}\n\n{to_avg}...',
                    fg='#84DFFF', font=RESULT_FONT)
        text.grid(column=1 , columnspan=1, pady=0)    
        image.thumbnail((200, 200), resample=Image.ANTIALIAS) 
        image_lbl = ImageTk.PhotoImage(image)
        result_image.config(image=image_lbl)
        result_image.grid(column=0, row=2, padx=10, sticky='e')
        result_image.image = image_lbl # keep a reference! so that the image will show
        
        


## Set up window
window = tk.Tk()
window.title("Typing Speed Test")
window.minsize(width=800, height=600)
window.config(bg=BACKGROUND_COLOR, padx=30, pady=30)


## Labels
title = tk.Label(text="How Fast Do You Type?", fg='#FFFCDC', bg=BACKGROUND_COLOR, font=TITLE_FONT)
title.grid(column=0, row=0, columnspan=3, pady=20)

instructions = tk.Label(text='Type the following text as is, when finished press ENTER.',justify="left", fg ='#FFFCDC' ,bg=BACKGROUND_COLOR, font=SUBTITLE_FONT)
instructions.grid(column=0, row=1, columnspan=2, padx=10, pady=15)

sample_text = choice(samples)
text = tk.Label(text=f'{sample_text}',justify="left", wraplength=650, fg ='#EDD2F3' ,bg=BACKGROUND_COLOR,  font=FONT)
text.grid(column=0, row=2, columnspan=2, padx=10, pady=0)

result_image = tk.Label(bg=BACKGROUND_COLOR)

try:
    with open('high_score.txt') as score:
        high_score = int(score.read())
except FileNotFoundError:
        high_score = 0
                
high_score_label = tk.Label(text=f'High Score: {high_score} WPM', fg ='#FFFCDC' ,bg=BACKGROUND_COLOR,  font=SUBTITLE_FONT)
high_score_label.grid(column=0, row=4, padx=10, sticky='w')

## Text
start=0
text_box = tk.Text(width=54, height=5, wrap='word', font=FONT, state='normal', bg='#fff')
text_box.grid(column=0, row=3, columnspan=3, padx=10, pady=20)
text_box.focus_set()
text_box.bind('<KeyPress>',timing)


## Buttons
refresh_button = tk.Button(text="Refresh", command=refresh_text, width=10, font=BUTTON_FONT)
refresh_button.grid(column=2, row=2,  sticky='n', padx=10, pady=10)

quit_button = tk.Button(text="Quit", command=window.destroy, width=10, font=BUTTON_FONT)
quit_button.grid(column=2, row=4, sticky='e', padx=10)


window.mainloop()
