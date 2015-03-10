declare -a arr=("j0" "j5" "jnoarea0" "jnoarea5" "jvoro")

for i in "${arr[@]}"
do
   echo "$i"
   python storemulti.py $i
done