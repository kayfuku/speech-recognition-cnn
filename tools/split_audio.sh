#!/bin/bash

# Split wav files into utterances. 
# executed in /home2/magics/corpora/fisher-english/fisher_eng_tr_sp_d1/

# echo "Hello world!"

input_path=./wav_test
# input_path=./wav

# For each wav file, make directory and split it. 
for wav_fold in $input_path/* 
do
    # echo $wav_fold # ./wav/000
    three_digits=${wav_fold##*/}
    # echo $three_digits # 000
    mkdir -p ./slices/$three_digits

    for wav_file_path in $wav_fold/*
    do
        # echo $wav_file_path # ./wav/000/fe_03_00001.wav
        wav_file_name=${wav_file_path##*/}
        # echo $wav_file_name # fe_03_00001.wav
        conversation_id=${wav_file_name%.*}
        # echo $conversation_id # fe_03_00001
        out_fold=./slices/$three_digits/${conversation_id}_slices
        mkdir -p $out_fold

        trans_file=../transcripts/data/trans/$three_digits/${conversation_id}.txt
        # echo $trans_file # ../transcripts/data/trans/000/fe_03_00001.txt

        # Read transcript file. 
        split_id=1
        while IFS="" read -r line
        do
            # echo $line 
            if [ ! -z "${line}" ]
            then
                start=$(echo $line | cut -d " " -f 1)
                end=$(echo $line | cut -d " " -f 2)
                channel=$(echo $line | cut -d " " -f 3)
                channel=${channel%:}
                # echo $start $end $channel # 3.76 5.54 A
                # echo $split_id
                out_file="${out_fold}/split-${split_id}-${conversation_id}_${channel}.wav"

                if [[ "$channel" = "A" ]]
                then
                    chan=1
                else
                    chan=2
                fi
                # echo $channel $chan # A 1

                sox "$wav_file_path" "$out_file" trim "$start" ="$end" remix $chan

                # sox "$wav_file_path" "$out_file" trim "$start" ="$end"
                # span=$end-$start
                # sox "$wav_file_path" "$out_file" trim "$start" "$span"

                let split_id=$split_id+1
            fi

        done < <(tail -n +3 $trans_file)

        echo "${three_digits} ${conversation_id} done."

    done

    # rm -rf "$wav_fold"

done


# # Read transcript file. 
# while IFS="" read -r line
# do
#     # echo $line 
#     if [ ! -z "${line}" ]
#     then
#         start=$(echo $line | cut -d " " -f 1)
#         end=$(echo $line | cut -d " " -f 2)
#         channel=$(echo $line | cut -d " " -f 3)
#         channel=${channel%:}
#
#         echo $start $end $channel
#     fi
#
# done < <(tail -n +3 ./fe_03_00001.txt)


# # Test
# awk '
#     NR == 1 {
#         print $0
#     }
#     NR > 2 {
#         if (length($0) > 0) 
#             start = $1
#             end = $2
#             channel = $3
#
#             system("sox --version")
#             # print start " " end " " channel
#             # print start
#
#     }
# ' ./fe_03_00001.txt


# # Test
# find . -name '*.wav' \
#  -exec sh -c 'mkdir -p ./slices/$(dirname "{}")' \; \
#  -exec sox {} ./slices/{} trim 3.76 =5.54 \;


# # Test
# var="/a/b/c.wav"
# dirname $var
# echo ${var%.*}



