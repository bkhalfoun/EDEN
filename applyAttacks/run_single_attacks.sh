trap 'echo "# $BASH_COMMAND"' DEBUG
urlTrain=$1  
urlTest=$2
xdays="$3"  #precise the background knowledge of the attack , e.g., 15days
dataset="$4"  #e.g., privamov
lppm="$5"   #which LPPM ? geoi , promesse or trl ? 
workdir="$6" #absolute path to save results
sc="$7"  #path to source code


possibleLog="$workdir""//log-AP-XXXXXXXXXXX.txt"
possibleLog1="$workdir""//log-POI-XXXXXXXXXXX.txt"
possibleLog2="$workdir""//log-PIT-XXXXXXXXXXX.txt"

#AP-attack 
cellSize="800.meters"
json_ap="$sc/ap-attack.json"
log_ap=$(mktemp "$possibleLog") 
java -jar  "$sc/"accio.jar run -workdir $workdir -params "urlTrain=$urlTrain urlTest=$urlTest cellSize=$cellSize"  $json_ap >> $log_ap
acc_ap=$(bash "$sc/"getRate.sh "AP-Attack rate" $log_ap)
echo "$acc_ap"
bash "$sc/"getCsv.sh $log_ap $workdir "MatMatchingKSetsnonObf/matches" "$workdir/"$xdays-ap-$lppm.csv

#POI-attack 
json_poi="$sc/poi-attack.json"
log_poi=$(mktemp $possibleLog1) 
java -jar  "$sc/"accio.jar run -workdir $workdir -params "urltrain=$urlTrain urltest=$urlTest"  $json_poi >> $log_poi 
acc_poi=$(bash "$sc/"getRate.sh "POI-Attack rate" $log_poi)
echo "$acc_poi"
bash "$sc/"getCsv.sh $log_poi $workdir "PoisReidentKSet/matches" "$workdir/"$xdays-poi-$lppm.csv


#PIT-attack
json_pit="$sc/pit-attack.json"
log_pit=$(mktemp $possibleLog2) 
java -jar  "$sc/"accio.jar run -workdir $workdir -params "urltrain=$urlTrain urltest=$urlTest"  $json_pit >> $log_pit
acc_pit=$(bash "$sc/"getRate.sh "PIT-Attack rate" $log_pit)
echo "$acc_pit"
bash "$sc/"getCsv.sh $log_pit $workdir "MMCReIdentKSet/matches" "$workdir/"$xdays-pit-$lppm.csv

echo "$dataset,$xdays,$lppm,AP-attack,$acc_ap" >> "$workdir/attacks.csv"  
echo "$dataset,$xdays,$lppm,POI-attack,$acc_poi" >> "$workdir/attacks.csv"  
echo "$dataset,$xdays,$lppm,PIT-attack,$acc_pit" >> "$workdir/attacks.csv"  
