import pandas as pd
import numpy as np
from konlpy.tag import Okt
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from tensorflow.python.keras.preprocessing.text import Tokenizer
from sklearn.model_selection import train_test_split
# https://uding.tistory.com/11

df = pd.read_csv('pred.csv')
