#!/bin/bash -xe

aux=1

for file in videos/*.3gp
do
  mkdir "images/$aux"
  ffmpeg -i "$file" -r 8 images/"$aux"/%04d.jpg
  for image in images/"$aux"/*.jpg
  do
    f=$(echo "$image" | cut -d \/ -f 3)
    convert $image -resize 50x50\! -quality 100 resized/"$aux.$f".jpg;

    convert resized/"$aux.$f".jpg rgb/"$aux.$f".txt

    n=$aux
    let "n-=1"
    echo "$(tail -n +2 rgb/"$aux.$f".txt  | cut -d " " -f 2 | cut -c2- | rev | cut -c2- | rev  | tr '\n' ',')$n"
  done >> dataset.csv

  let "aux+=1"
done
