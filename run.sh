# coding:utf-8
#/bin/bash
function terminate() {
  exit
}
trap 'terminate' {1,2,3,15}

echo "Start"

for obj in 'bagel' 'cable_gland' 'carrot' 'cookie' 'dowel' 'foam' 'peach' 'potato' 'rope' 'tire'
do
  python mvtec3d_show.py --obj $obj
done

<< COMMENTOUT

COMMENTOUT