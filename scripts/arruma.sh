for d in `ls`;
do
	if [ -d $d ]
	then
		echo "random $d"
		mkdir -p $d/random/percent
		mv $d/*_random_percent_* $d/random/percent
		mkdir -p $d/random/fixed
		mv $d/*_random_selected_* $d/random/fixed/

		echo "ksampler $d"
		mkdir -p $d/ksampler/percent
		mv $d/*_ksampler_percent_* $d/ksampler/percent/
		mkdir -p $d/ksampler/fixed
		mv $d/*_ksampler_selected_* $d/ksampler/fixed/

		echo "bernoulli $d"
		mkdir -p $d/bernoulli
		mv $d/*_bernouli_selected_* $d/bernoulli/
	fi
done
