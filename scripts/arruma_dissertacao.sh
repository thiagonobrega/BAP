rename 's/drugs_ca/drugsca/' *.pkl
rename 's/drugs_fda/drugsfda/' *.pkl
rename 's/parsed_cnef/cnefe/' *.pkl
rename 's/parsed_iptu/iptu/' *.pkl
rename 's/parsed_lei/lei/' *.pkl
rename 's/parsed_sec/sec/' *.pkl
rename 's/tripadvisor_data/tripadvisor/' *.pkl
rename 's/yelp_data/yelp/' *.pkl

##
## actual
##

#base
rename 's/ohio_voters/ohio/' *.pkl
rename 's/parsed_lei/lei/' *.pkl
rename 's/parsed_sec/sec/' *.pkl
rename 's/tripadvisor_data/tripadvisor/' *.pkl
rename 's/yelp_data/yelp/' *.pkl

# full
rename 's/\.pkl/\_full\_1\.pkl/' *.pkl

#simples (testar)
rename 's/p0/0\./' *.pkl

#combinado
#rename 's/\.0/0/' *.pkl
rename 's/\.0//' *.pkl


####
#### Sort File
####

mkdir ca
mkdir fda

mkdir mpog
mkdir cgu

mkdir nc
mkdir oh

mkdir trip
mkdir yelp

mv cgu*.pkl cgu/
mv mpog*.pkl mpog/

mv drugsfda*.pkl fda/
mv drugsca*.pkl ca/

mv ncvoter*.pkl nc/
mv ohio*.pkl oh/

mv tripadvisor*.pkl trip/
mv yelp*.pkl yelp/


mkdir cnefe
mkdir iptu

mkdir lei
mkdir sec

mv parsedcnef*.pkl cnefe/
mv parsediptu*.pkl iptu/

mv lei*.pkl lei/
mv sec*.pkl sec/

#### chec
ls ca/ | wc -l
ls cgu/ | wc -l
ls cnefe/ | wc -l
ls fda | wc -l
ls iptu | wc -l
ls lei/ | wc -l
ls mpog/ | wc -l
ls nc | wc -l
ls oh | wc -l
ls sec | wc -l
ls trip/ | wc -l
ls yelp/ | wc -l
