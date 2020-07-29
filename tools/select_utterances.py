# executed in /home2/magics/corpora/fisher-english/fisher_eng_tr_sp_d1/

import pandas as pd
import numpy as np
import csv, os
import pprint
import pathlib
import shutil


def main():
  # label_filename = 'utter_top4.csv'
  label_file_stem = 'lang70_region'
  labels_path = 'label_data/' + label_file_stem + '.csv'
  input_utterances_path = './slices'
  out_dir = 'selected_utterances_' + label_file_stem + '_v1.5'

  os.makedirs(out_dir)

  utterances_labels = pd.read_csv(labels_path)
  selected_file_names = set(utterances_labels['FILENAME'])

  utterances_dir = pathlib.Path(input_utterances_path)
  count = 0
  for utterance_file in utterances_dir.glob('**/*.wav'):
    # pprint.pprint(utterance_file) # PosixPath('slices/000/fe_03_00001_slices/split-2-fe_03_00001_A.wav')
    # print(utterance_file.stem) # split-2-fe_03_00001_A
    filename = utterance_file.name
    # print(filename) # split-2-fe_03_00001_A.wav

    if filename in selected_file_names:
      shutil.copy(utterance_file, out_dir)
      count += 1
      if count % 1000 == 0:
        print(count)
      if count == 50000:
        break

  print('count:', count)
  print('done.')


if __name__ == '__main__':
  main()
