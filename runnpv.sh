declare -a arr=("j0" "j5" "jnoarea0" "jnoarea5")

for i in "${arr[@]}"
do
   echo "$i"
   python storenpv.py $i
done