for i in "0.1" "0.01" "0.001" "0.0001" "0.2" "0.02" "0.002" "0.0002" "0.5" "0.05" "0.005" "0.0005" "Discrete"
do

cd "$i"
python3 plotting.py

cd ../

done


