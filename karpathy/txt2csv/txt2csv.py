import os
import sys
import time
import shutil
import pickle
import pandas as pd

from utils2 import Config

if not os.path.exists(Config.csv_dir):
  print('creating ', Config.csv_dir)
  os.makedirs(Config.csv_dir)

have = set(os.listdir(Config.csv_dir))
files = os.listdir(Config.txt_dir)
for i,f in enumerate(files): # there was a ,start=1 here that I removed, can't remember why it would be there. shouldn't be, i think.

  csv_basename = f + '.csv'
  if csv_basename in have:
    print('%d/%d skipping %s, already exists.' % (i, len(files), csv_basename, ))
    continue

  txt_path = os.path.join(Config.txt_dir, f)
  csv_path = os.path.join(Config.csv_dir, csv_basename)
  
  file1=open(txt_path, encoding='utf-8')
  lines = file1.read().split(' ')
  pd.Series(lines).to_csv(csv_path)
     
  file1.close()

  print('%d/%d' % (i, len(files)))

  # check output was made
  if not os.path.isfile(csv_path):
    # there was an error with converting the pdf
    print('there was a problem with parsing %s to text, creating an empty text file.' % (txt_path, ))
    os.system('touch ' + csv_path) # create empty file, but it's a record of having tried to convert

  time.sleep(0.01) # silly way for allowing for ctrl+c termination