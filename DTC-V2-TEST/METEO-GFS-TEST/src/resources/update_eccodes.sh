#!bin/bash
echo $2
if [ !  -z "$2" ];then
		
	path4="$1/definitions/grib2/localConcepts/$2/name.def"
	path1="$1/definitions/grib2/localConcepts/$2/shortName.def"
	path5="$1/definitions/grib2/localConcepts/$2/paramId.def"
	path6="$1/definitions/grib2/localConcepts/$2/units.def"
        parameter_n=196
	array_paths=($path1)
else	
	path1="$1/definitions/grib2/shortName.def"
	path2="$1/definitions/grib2/cfVarName.def"
	path4="$1/definitions/grib2/name.def"
	path5="$1/definitions/grib2/paramId.def"
	path6="$1/definitions/grib2/units.def"
	parameter_n=18
	array_paths=($path1 $path2)
fi





for file in ${array_paths[@]};  do 
	if [ -f "$file" ]; then
		if grep -q hpbl "$file"; then
			echo "Variable hpbl has been added before to the $file"
		else
			echo "Adding hpbl variable to $file"   
			touch $file
			echo "#Planetary boundary layer height" >> $file
			echo "'hpbl' = { ">> $file
			echo "         discipline = 0 ;" >> $file
			echo "         parameterCategory = 3 ;" >> $file
			echo "         parameterNumber = $parameter_n ;" >> $file
			echo "        }">> $file
			cat $file
		fi 

	else
		echo "not file $file"
	fi 
done
if [ -f "$path4" ];then 
	if grep -q "Planetary boundary layer height" "$path4"; then
		echo "Variable hpbl has been added before to the $path4"
	else
		echo "Adding hpbl variable to $path4"   
		touch $path4
		echo "#Planetary boundary layer height" >> $path4
		echo "'Planetary boundary layer height' = { ">> $path4
		echo "         discipline = 0 ;" >> $path4
		echo "         parameterCategory = 3 ;" >> $path4
		echo "         parameterNumber = $parameter_n ;" >> $path4
		echo "        }">> $path4
		cat $path4
	fi 
else
	echo "not file $path4"	
fi

if [ -f "$path5" ];then 
	if grep -q "Planetary boundary layer height" "$path5"; then
		echo "Variable hpbl has been added before to the $path5"
	else
		echo "Adding hpbl variable to $path5"   
		touch $path5
		echo "#Planetary boundary layer height" >> $path5
		echo "'260083' = { ">> $path5
		echo "         discipline = 0 ;" >> $path5
		echo "         parameterCategory = 3 ;" >> $path5
		echo "         parameterNumber = $parameter_n ;" >> $path5
		echo "        }">> $path5
		cat $path5
	fi 
else
	echo "not file $path5"	
fi

if [ -f "$path6" ];then
        if grep -q "Planetary boundary layer height" "$path6"; then
                echo "Variable hpbl has been added before to the $path6"
        else
                echo "Adding hpbl variable to $path6"
                touch $path6
                echo "#Planetary boundary layer height" >> $path6
                echo "'m' = { ">> $path6
                echo "         discipline = 0 ;" >> $path6
                echo "         parameterCategory = 3 ;" >> $path6
                echo "         parameterNumber = $parameter_n ;" >> $path6
                echo "        }">> $path6
                cat $path6
        fi
else            
        echo "not file $path6"
fi

