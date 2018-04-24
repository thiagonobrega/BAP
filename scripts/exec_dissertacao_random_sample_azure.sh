echo ":::: Simples"
#echo "SP"
time python3 calculate_Signatures.py -process 8 -dt sp_cnefe -s 1 -encrypt 256 /home/thiago/samples/SP_Adresses/cnefe/simples/ |&  tee random_simple_sp_cnefe.log
time python3 calculate_Signatures.py -e iso-8859-1 -process 8 -dt sp_iptu -s 1 -encrypt 256 /home/thiago/samples/SP_Adresses/iptu/simples/ |&  tee random_simple_sp_iptu.log

echo "FEII"
time python3 calculate_Signatures.py -process 8 -dt feii_lei -s 1 -encrypt 256 /home/thiago/samples/feii/lei/simples/ |&  tee random_simple_feii_lei.log
time python3 calculate_Signatures.py -process 8 -dt feii_sec -s 1 -encrypt 256 /home/thiago/samples/feii/sec/simples/ |&  tee random_simple_feii_sec.log

echo "US_VOTERS"
time python3 calculate_Signatures.py -dt voters_nc -s 1 -process 8 -encrypt 1024 /home/thiago/samples/us_voters/nc/simples/ |& tee log_full_ncvoters.log
time python3 calculate_Signatures.py -dt voters_ohio -s 1 -process 8 -encrypt 1024 /home/thiago/samples/us_voters/oh/simples/|& tee log_ohiovoters.log

echo "REST"
time python3 calculate_Signatures.py -dt rest_tripadvisor -s 1 -process 8 -encrypt 2048 /home/thiago/samples/Restaurants/trip/simples/ |& tee random_simple_log_trip.log
time python3 calculate_Signatures.py -dt rest_yelp -s 1 -process 8 -encrypt 2048 /home/thiago/samples/Restaurants/yelp/simples/ |& tee random_simple_log_yelp.log

echo "DRUGS"
time python3 calculate_Signatures.py -process 8 -dt drugs_fda -s 1 -encrypt 1024 /home/thiago/samples/drugs/fda/simples/ |& tee random_simple_drugs_fda.log
time python3 calculate_Signatures.py -process 8 -dt drugs_ca -s 1 -encrypt 1024 /home/thiago/samples/drugs/ca/simples/ |& tee random_simple_drugs_ca.log

echo "PE"
time python3 calculate_Signatures.py -process 8 -dt pe_mpog -s 1 -encrypt 2048 /home/thiago/samples/PublicEmployees/mpog/simples/ |&  tee random_simple_pe_mpgo.log
time python3 calculate_Signatures.py -process 8 -dt pe_cgu -s 1 -encrypt 2048 /home/thiago/samples/PublicEmployees/cgu/simples/ |& tee random_simple_pe_cgu.log

mkdir /home/thiago/pyPAS/data/signatures/random_simples
mv /home/thiago/pyPAS/data/signatures/*.pkl /home/thiago/pyPAS/data/signatures/random_simples/

echo ":::: Combinado"

echo "REST"
time python3 calculate_Signatures.py -dt rest_tripadvisor -s 1 -process 8 -encrypt 2048 /home/thiago/samples/Restaurants/trip/combinado/ |& tee random_combinado_log_trip.txt
time python3 calculate_Signatures.py -dt rest_yelp -s 1 -process 8 -encrypt 2048 /home/thiago/samples/Restaurants/yelp/combinado/ |& tee random_combinado_log_yelp.txt

echo "FEII"
time python3 calculate_Signatures.py -process 8 -dt feii_lei -s 1 -encrypt 256 /home/thiago/samples/feii/lei/combinado/ |&  tee random_combinado_feii_lei.log
time python3 calculate_Signatures.py -process 8 -dt feii_sec -s 1 -encrypt 256 /home/thiago/samples/feii/sec/combinado/ |&  tee random_combinado_feii_sec.log

echo "US_VOTERS"
time python3 calculate_Signatures.py -dt voters_nc -s 1 -process 8 -encrypt 1024 /home/thiago/samples/us_voters/nc/combinado/ |& tee log_full_ncvoters.log
time python3 calculate_Signatures.py -dt voters_ohio -s 1 -process 8 -encrypt 1024 /home/thiago/samples/us_voters/oh/combinado/|& tee log_ohiovoters.log

echo "DRUGS"
time python3 calculate_Signatures.py -process 8 -dt drugs_fda -s 1 -encrypt 1024 /home/thiago/samples/drugs/fda/combinado/ |& tee random_combinado_drugs_fda.log
time python3 calculate_Signatures.py -process 8 -dt drugs_ca -s 1 -encrypt 1024 /home/thiago/samples/drugs/ca/combinado/ |& tee random_combinado_drugs_ca.log

echo "PE"
time python3 calculate_Signatures.py -process 8 -dt pe_mpog -s 1 -encrypt 2048 /home/thiago/samples/PublicEmployees/mpog/combinado/ |&  tee random_combinado_pe_mpgo.log
time python3 calculate_Signatures.py -process 8 -dt pe_cgu -s 1 -encrypt 2048 /home/thiago/samples/PublicEmployees/cgu/combinado/ |& tee random_combinado_pe_tce.log

echo "SP"
time python3 calculate_Signatures.py -process 8 -dt -e iso-8859-1 sp_cnefe -s 2 -encrypt 256 /home/thiago/samples/SP_Adresses/cnefe/combinado/ |&  tee random_combinado_sp_cnefe.log
time python3 calculate_Signatures.py -process 8 -dt sp_iptu -s 2 -encrypt 256 /home/thiago/samples/SP_Adresses/iptu/combinado/ |&  tee random_combinado_sp_iptu.log

mkdir /home/thiago/pyPAS/data/signatures/random_combinado
mv /home/thiago/pyPAS/data/signatures/*.pkl /home/thiago/pyPAS/data/signatures/random_combinado/

echo ":::: Full"
time python3 calculate_Signatures.py -file True -e iso-8859-1 -process 8 -dt sp_cnefe -s 1 -encrypt 256 /home/thiago/dados/SP_Adresses/parsedcnef.csv |&  tee sp_cnefe.log
time python3 calculate_Signatures.py -file True -process 4 -dt sp_iptu -s 2 -encrypt 256 /home/thiago/dados/SP_Adresses/parsediptu.csv |&  tee sp_iptu.log

mkdir /home/thiago/pyPAS/data/signatures/full
mv /home/thiago/pyPAS/data/signatures/*.pkl /home/thiago/pyPAS/data/signatures/full/

 