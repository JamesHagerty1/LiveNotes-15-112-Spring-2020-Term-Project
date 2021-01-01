DESCRIPTION:

LiveNotes was my Spring 2020 term project for 15-112, Fundamentals of Programming and Computer Science at Carnegie Mellon University.  It is a text editor with the look of a notebook.  It has a broad, unique set of features. 

A demonstration video: https://www.youtube.com/watch?v=AvQ6pm2Kk7w&feature=youtu.be


SETUP AND USE INSTRUCTIONS:

1. You will need to install these external libraries that LiveNotes imports: 'import requests' and 'from bs4 import BeautifulSoup' and 'import speech_recognition as sr'.  

2. Download the following files and place all of them in the same folder: LivesNotes.py, cmu_112_graphics.py, Images.py, Page.py, Files.py, Tables.py, Autnotes.py, Symbols.py, Grammar.py, Text.py, words.pkl and moreCommonWords.pkl.


INFLUENCES AND LIMITATIONS: 

Because LiveNotes was a class project, I followed standards set by 15-112, for this specific term project.  For example, I was instructed to create my entire term project in Python, which is why LiveNotes was created entirely in Python.  In 15-112, I was taught to use Python's TkInter, which is why this text editor is a TkInter GUI.  I was also instructed to create as many features from scratch as I could, to earn "complexity points" to maximize my term project grade.  That is why functionalities like copying and pasting text or spellchecking were created from scratch, even if it would have typically made more sense to rely on libraries and built-in features to use such common functionalities. 

Note: you can only open images in the LiveNotes GUI if those images are placed in the same folder as the other files discussed in SETUP AND USE INSTRUCTIONS (this is a limitation of the graphics library LiveNotes uses).