kw="Run"
f=$1
workdir=$2
key=$3

line=$(grep "$kw" $f) 
IFS=': '; read -r -a array <<< "$line"

startID="${array[1]}"
#echo "$startID"

for out in $workdir/run-$startID*
do
	#echo "$out"
	runFile="$out"
done 


#jq -r ".report.artifacts  | .[] | select(.name==\"$key\") | .value | to_entries[] | [.key, .value] | @csv" $run > tmp.csv
jq -r ".report.artifacts  | .[] | select(.name==\"$key\") | .value | .uri" $runFile



#for index in "${!array[@]}"
#do
#    echo "$index ${array[index]}"
#done 
#pour recuperer le chemin des donnee protegée 
