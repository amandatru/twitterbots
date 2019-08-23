#!/bin/bash
# declare STRING variable
STRING="Starting script..."
#print variable on a screen
echo $STRING
#
# read -t my_array < <( ls $search_path | grep *.mkv  )
# printf '%s\n' "${my_array[@]}"
files=(*.mkv)
count=0

# echo $count
# echo "${files[@]}"

for file in "${files[@]}"; do
    count=$((count+1))
     #note that I commented everything out and uncommented mkdir first to generate the script
    # mkdir $count
    ffmpeg -i $file -ss 300 -qscale:v 10 -vf fps=1/30 ./$count/%03d.png
    # echo "$file"
done

# for file in "${files[@]}"; do
#     mkdir $count
#     echo "$file"
# done
