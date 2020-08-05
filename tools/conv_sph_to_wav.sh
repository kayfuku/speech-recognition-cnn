#!/bin/bash

# Convert sph to wav.
# executed in /home2/magics/corpora/fisher-english/fisher_eng_tr_sp_d1/

input_path=./audio

for sph_fold in $input_path/*
do 
	# echo $sph_fold # ./audio/001
	three_digits=${sph_fold##*/}
	# echo $three_digits # 001

	mkdir -p ./wav/$three_digits

	for sph_file_path in $sph_fold/*.sph
	do
		# echo $sph_file_path # ./audio/001/fe_03_00100.sph
        sph_file_name=${sph_file_path##*/}
        # echo $sph_file_name # fe_03_00100.sph
        conversation_id=${sph_file_name%.*}
        # echo $conversation_id # fe_03_00100
		out_path=./wav/$three_digits/${conversation_id}.wav
		# echo $out_path # ./wav/001/fe_03_00100.wav

		# sox -t sph "$sph_file_path" -b 16 -t wav "$out_path"
		# This is an alternative code for the line above using sph2pipe. 
		sph2pipe -p -f wav "$sph_file_path" "$out_path"

		echo $conversation_id "done."

	done

	echo $three_digits "done."

done

echo "done."































