import librosa
import os
import pathlib
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.preprocessing import LabelEncoder


# Convert to feature.
def wav2feature(file_path, feature_type, feature_height=20, max_len_time=100):
  # print(file_path) # selected_utterances/split-1-fe_03_00004_A.wav
  # wave, sr = librosa.load(file_path, duration=5)
  wave, sr = librosa.load(file_path, sr=None, duration=5)
  assert sr == 8000
  # print(sr)
  # print(len(wave)) # 11200

  if feature_type == "mfcc":
    # mfcc
    feature = librosa.feature.mfcc(y=wave, sr=sr, n_mfcc=feature_height)
  else:
    # log_mel
    feature = librosa.feature.melspectrogram(y=wave, sr=sr, n_mels=feature_height)
    feature = librosa.power_to_db(feature)

  # print(feature.shape)  # (25, 215) <= (frequency, time)

  # Padding (time axis)
  if max_len_time > feature.shape[1]:
    pad_width = max_len_time - feature.shape[1]
    feature = np.pad(feature, pad_width=((0, 0), (0, pad_width)), mode='constant')
  else:
    # Cut off the remaining parts.
    feature = feature[:, :max_len_time]

  # print(feature)
  # print(feature.shape)

  return feature


def save_features_and_get_labels(wav_path, labels_table_path, feature_type,
                                 save=True, feature_path=None,
                                 feature_height=20, max_len_time=100):
  feature_vectors = []
  labels = []
  print('feature_height:', feature_height)
  print('max_len_time:', max_len_time)

  # Create DataFrame for labels.
  utterances_labels = pd.read_csv(labels_table_path)
  # Label encoder
  le = LabelEncoder()
  utterances_labels['LABEL'] = le.fit_transform(utterances_labels['LABEL'])
  label_map = le.classes_

  print('Generating labels ...')
  if save:
    print('Generating {} ...'.format(feature_type))

  wav_dir = pathlib.Path(wav_path)
  count = 0
  for wav_file_path in wav_dir.glob('*.wav'):
    if save:
      # Convert wav to feature (mfcc/log_mel)
      feature = wav2feature(wav_file_path, feature_type, feature_height, max_len_time)
      feature_vectors.append(feature)

    label = utterances_labels[utterances_labels['FILENAME'] == wav_file_path.name]['LABEL'].values[0]
    labels.append(label)

    count += 1
    if count % 500 == 0:
      if save:
        print('wav to {}, {} done.'.format(feature_type, count))
      else:
        print('{} done.'.format(count))
      # if count == 10000:
      #   break

  if save:
    np.save(feature_path, feature_vectors)

  return labels, label_map


def get_train_test(feature_path, labels, test_size=0.2, random_state=41):
  X = np.load(feature_path)
  # print(X.shape) # (10000, 25, 215)
  # print(labels) # [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
  labels = np.array(labels).reshape(1, len(labels)).T

  return train_test_split(X, labels, test_size=test_size, random_state=random_state, shuffle=True)



# WAV_PATH = "./selected_utterances/"
# MFCC_PATH = "mfcc/mfcc.npy"
# LABELS_TABLE_PATH = 'label_data/utter_top4.csv'
# MAX_LEN_TIME = 75
# N_MFCC = 20
#
# labels, label_map = save_mfcc_and_labels(WAV_PATH, LABELS_TABLE_PATH, MFCC_PATH, MAX_LEN_TIME, N_MFCC)
#
# X_train, X_test, y_train, y_test = get_train_test(MFCC_PATH, labels)
# print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
#
#
# print('done.')
# print('test')













