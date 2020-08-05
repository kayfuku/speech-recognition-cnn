# Make file_listing.csv 

import pandas as pd
import numpy as np
import csv, os
import pprint
import pathlib


def main():
    # Set output file name.
    out_file = 'file_listing.csv'
    if os.path.exists(out_file):
        os.remove(out_file)

    # Set paths.
    pindata_path = '/home2/magics/corpora/fisher-english/transcripts/doc/part1/fe_03_pindata.tbl'
    calldata1_path = '/home2/magics/corpora/fisher-english/transcripts/doc/part1/fe_03_p1_calldata.tbl'
    calldata2_path = '/home2/magics/corpora/fisher-english/transcripts/doc/part2/fe_03_p2_calldata.tbl'
    trans_path = 'transcripts/data/trans'
    # # Set paths for testing.
    # pindata_path = 'file_listing/data/fe_03_pindata.tbl'
    # calldata1_path = 'file_listing/data/fe_03_p1_calldata.tbl'
    # calldata2_path = 'file_listing/data/fe_03_p2_calldata.tbl'
    # trans_path = 'transcripts/data/trans'


    # Create tables.
    pindata = pd.read_csv(pindata_path)
    calldata1 = pd.read_csv(calldata1_path)
    calldata2 = pd.read_csv(calldata2_path)
    pindata_sub = pindata[['PIN', 'S_SEX', 'S_AGE', 'EDU', 'NATIVE_LANG', 'WHERE_RAISED']]
    calldata1_sub = calldata1[['CALL_ID', 'TOPICID', 'APIN', 'ASX.DL', 'BPIN', 'BSX.DL']]
    calldata2_sub = calldata2[['CALL_ID', 'TOPICID', 'APIN', 'ASX.DL', 'BPIN', 'BSX.DL']]
    calldata_concat = pd.concat([calldata1_sub, calldata2_sub])
    calldata_concat = calldata_concat.reset_index(drop=True)

    # Traverse the transcript files.
    trans_root_dir = pathlib.Path(trans_path)
    for trans_file in trans_root_dir.glob('**/*.txt'):
        # pprint.pprint(trans_file) # PosixPath('transcripts/data/trans/000/fe_03_00001.txt')
        # print(trans_file.stem) # fe_03_00001

        conversation_id = trans_file.stem
        call_id = conversation_id[-5:]
        three_digits = call_id[0:3]
        # print('call_id:', call_id) # call_id: 00001
        # print('conversation_id:', conversation_id) # conversation_id: fe_03_00001
        # print('three_digits:', three_digits) # three_digits: 000

        # Get labels.
        row_calldata = calldata_concat[calldata_concat['CALL_ID'] == int(call_id)]
        topic = row_calldata['TOPICID'].values[0]
        labels_for_each_channel = dict()
        for channel_id in ['A', 'B']:
            if channel_id == 'A':
                pin = row_calldata['APIN'].values[0]
                sxdl = row_calldata['ASX.DL'].values[0]
            else:
                pin = row_calldata['BPIN'].values[0]
                sxdl = row_calldata['BSX.DL'].values[0]

            row_pindata = pindata_sub[pindata_sub['PIN'] == pin]

            labels = row_pindata.values.squeeze()
            labels = np.append(labels, [topic, sxdl])

            labels_for_each_channel[channel_id] = labels


        # pprint.pprint(labels_for_each_channel)

        # Read from transcript file.
        with open(trans_file, encoding='utf_8') as f:
            data = []
            split_id = 1
            for line in f:
                if not line.startswith('#') and line.strip():
                    # Get channel.
                    tokens = line.split()
                    channel = tokens[2]
                    channel_id = channel[:1]

                    utterance_file_path = 'slices/' + three_digits + '/' + conversation_id + '_slices/split-' + \
                                str(split_id) + '-' + conversation_id + '_' + channel_id + '.wav'

                    labels_with_file_path = []
                    labels_with_file_path.append(utterance_file_path)
                    labels_with_file_path.extend(labels_for_each_channel[channel_id])
                    data.append(labels_with_file_path)

                    split_id += 1


        # Write out (append) the labels.
        with open(out_file, mode='a') as f:
            writer = csv.writer(f)

            writer.writerow("file_path, pin, gender_reported_by_speaker, education, native_lang, where_raised, topic, [gender_reported_by_auditor].[american_or_other_eng]")
            for line in data:
                # print(line)
                writer.writerow(line)


        print(conversation_id + ' done.')


    print('done.')










if __name__ == '__main__':
    main()
