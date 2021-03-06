# -*- coding: utf-8 -*-
"""Tradutor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cMnBIfdBDRzey2ZPQHQPnq1jIeC1Ycaj
"""

!pip install deep_translator
#import pandas as pd


from deep_translator import GoogleTranslator
translated = GoogleTranslator(source='auto', target='de').translate("keep it up, you are awesome")

from deep_translator import (GoogleTranslator,
                             PonsTranslator,
                             LingueeTranslator,
                             MyMemoryTranslator,
                             YandexTranslator,
                             DeepL,
                             QCRI,
                             single_detection,
                             batch_detection)

text = 'Hello'
#translated = GoogleTranslator(source='en', target='portuguese').translate_file('path/to/file')
translated = GoogleTranslator(source='en', target='portuguese').translate(text=text)

print(translated)