echo ":::: Simples"
echo "SP"
time python3 calculate_Signatures.py -process 8 -dt sp_cnefe -s 2 -encrypt 256 /home/thiagonobrega/zexp/samples/SP_Adresses/cnefe/simples/ |&  tee random_simple_sp_cnefe.log
time python3 calculate_Signatures.py -e iso-8859-1 -process 8 -dt sp_iptu -s 2 -encrypt 256 /home/thiagonobrega/zexp/samples/SP_Adresses/iptu/simples/ |&  tee random_simple_sp_iptu.log

echo "FEII"
time python3 calculate_Signatures.py -process 8 -dt feii_lei -s 2 -encrypt 256 /home/thiagonobrega/zexp/samples/feii/lei/simples/ |&  tee random_simple_feii_lei.log
time python3 calculate_Signatures.py -process 8 -dt feii_sec -s 2 -encrypt 256 /home/thiagonobrega/zexp/samples/feii/sec/simples/ |&  tee random_simple_feii_sec.log

echo "DRUGS"
time python3 calculate_Signatures.py -process 8 -dt drugs_fda -s 2 -encrypt 1024 /home/thiagonobrega/zexp/samples/drugs/fda/simples/ |& tee random_simple_drugs_fda.log
time python3 calculate_Signatures.py -process 8 -dt drugs_ca -s 2 -encrypt 1024 /home/thiagonobrega/zexp/samples/drugs/ca/simples/ |& tee random_simple_drugs_ca.log

echo "PE"
time python3 calculate_Signatures.py -process 8 -dt pe_mpog -s 2 -encrypt 256 /home/thiagonobrega/zexp/samples/PublicEmployees/mpog/simples/ |&  tee random_simple_pe_mpgo.log
time python3 calculate_Signatures.py -process 8 -dt pe_tce -s 2 -encrypt 256 /home/thiagonobrega/zexp/samples/PublicEmployees/tce/simples/ |& tee random_simple_pe_tce.log

echo "REST"
time python3 calculate_Signatures.py -dt rest_tripadvisor -s 2 -process 8 -encrypt 2048 /home/thiagonobrega/zexp/samples/Restaurants/trip/simples/ |& tee random_simple_log_trip.txt
time python3 calculate_Signatures.py -dt rest_yelp -s 2 -process 8 -encrypt 2048 /home/thiagonobrega/zexp/samples/Restaurants/yelp/simples/ |& tee random_simple_log_yelp.txt

mkdir /home/thiagonobrega/zexp/pyPAS/data/signatures/random_simples
mv /home/thiagonobrega/zexp/pyPAS/data/signatures/*.pkl /home/thiagonobrega/zexp/pyPAS/data/signatures/random_simples/

echo ":::: Combinado"
echo "SP"
time python3 calculate_Signatures.py -process 8 -dt sp_cnefe -s 2 -encrypt 256 /home/thiagonobrega/zexp/samples/SP_Adresses/cnefe/combinado/ |&  tee random_combinado_sp_cnefe.log
time python3 calculate_Signatures.py -e iso-8859-1 -process 8 -dt sp_iptu -s 2 -encrypt 256 /home/thiagonobrega/zexp/samples/SP_Adresses/iptu/combinado/ |&  tee random_combinado_sp_iptu.log

echo "FEII"
time python3 calculate_Signatures.py -process 8 -dt feii_lei -s 2 -encrypt 256 /home/thiagonobrega/zexp/samples/feii/lei/combinado/ |&  tee random_combinado_feii_lei.log
time python3 calculate_Signatures.py -process 8 -dt feii_sec -s 2 -encrypt 256 /home/thiagonobrega/zexp/samples/feii/sec/combinado/ |&  tee random_combinado_feii_sec.log

echo "DRUGS"
time python3 calculate_Signatures.py -process 8 -dt drugs_fda -s 2 -encrypt 1024 /home/thiagonobrega/zexp/samples/drugs/fda/combinado/ |& tee random_combinado_drugs_fda.log
time python3 calculate_Signatures.py -process 8 -dt drugs_ca -s 2 -encrypt 1024 /home/thiagonobrega/zexp/samples/drugs/ca/combinado/ |& tee random_combinado_drugs_ca.log

echo "PE"
time python3 calculate_Signatures.py -process 8 -dt pe_mpog -s 2 -encrypt 256 /home/thiagonobrega/zexp/samples/PublicEmployees/mpog/combinado/ |&  tee random_combinado_pe_mpgo.log
time python3 calculate_Signatures.py -process 8 -dt pe_tce -s 2 -encrypt 256 /home/thiagonobrega/zexp/samples/PublicEmployees/tce/combinado/ |& tee random_combinado_pe_tce.log

echo "REST"
time python3 calculate_Signatures.py -dt rest_tripadvisor -s 2 -process 8 -encrypt 2048 /home/thiagonobrega/zexp/samples/Restaurants/trip/combinado/ |& tee random_combinado_log_trip.txt
time python3 calculate_Signatures.py -dt rest_yelp -s 2 -process 8 -encrypt 2048 /home/thiagonobrega/zexp/samples/Restaurants/yelp/combinado/ |& tee random_combinado_log_yelp.txt

mkdir /home/thiagonobrega/zexp/pyPAS/data/signatures/random_combinado
mv /home/thiagonobrega/zexp/pyPAS/data/signatures/*.pkl /home/thiagonobrega/zexp/pyPAS/data/signatures/random_combinado/

 