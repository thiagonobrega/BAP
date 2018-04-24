echo "US_VOTERS"
time python3 calculate_Signatures.py -file True -dt voters_nc -s 4 -process 8 -encrypt 1024 /home/thiago/dados/us_voters/ncvoter.csv |& tee log_full_ncvoters.log
time python3 calculate_Signatures.py -file True -dt voters_ohio -s 4 -process 8 -encrypt 1024 /home/thiago/dados/us_voters/ohio_voters.csv |& tee log_ohiovoters.log

echo "FEII"
time python3 calculate_Signatures.py -file True -process 8 -dt feii_lei -s 2 -encrypt 256 /home/thiago/dados/fei/parsed_lei.csv |&  tee log_ful_feii_lei.log
time python3 calculate_Signatures.py -file True -process 8 -dt feii_sec -s 2 -encrypt 256 /home/thiago/dados/fei/parsed_sec.csv |&  tee log_ful_feii_sec.log

echo "DRUGS"
time python3 calculate_Signatures.py -file True -process 4 -dt drugs_fda -s 4 -encrypt 1024 /home/thiago/dados/drugs/drugsfda.csv |& tee log_ful_drugs_fda.log
time python3 calculate_Signatures.py -file True -process 4 -dt drugs_ca -s 4 -encrypt 1024 /home/thiago/dados/drugs/drugsca.csv |& tee log_ful_drugs_ca.log

echo "PE"
time python3 calculate_Signatures.py -file True -process 8 -dt pe_mpog -s 2 -encrypt 2048 /home/thiago/dados/PublicEmployees/mpog.csv |&  tee log_ful_pe_mpgo.log
time python3 calculate_Signatures.py -file True -process 8 -dt pe_cgu -s 2 -encrypt 2048 /home/thiago/dados/PublicEmployees/cgu.csv |& tee log_ful_pe_cgu.log

echo "REST"
time python3 calculate_Signatures.py -file True -dt rest_tripadvisor -s 2 -process 8 -encrypt 2048 /home/thiago/dados/Restaurants/tripadvisor_data.csv |& tee log_ful_log_trip.log
time python3 calculate_Signatures.py -file True -dt rest_yelp -s 2 -process 8 -encrypt 2048 /home/thiago/dados/Restaurants/yelp_data.csv |& tee log_ful_log_yelp.log

mkdir /home/thiago/pyPAS/data/signatures/full
mv /home/thiago/pyPAS/data/signatures/*.pkl /home/thiago/pyPAS/data/signatures/full/

















































































echo "SP"
time python3 calculate_Signatures.py -file True -process 4 -dt sp_cnefe -s 2 -encrypt 256 /home/thiago/dados/SP_Adresses/parsedcnef.csv |&  tee sp_cnefe.log
time python3 calculate_Signatures.py -e iso-8859-1 -file True -process 4 -dt sp_iptu -s 2 -encrypt 256 /home/thiago/dados/SP_Adresses/parsediptu.csv |&  tee sp_iptu.log
#time python3 calculate_Signatures.py -file True -process 8 -dt sp_cnefe -s 2 -encrypt 256 /home/thiagonobrega/zexp/odata/SP_Adresses/parsed_cnef.csv |&  tee sp_cnefe.log
#time python3 calculate_Signatures.py -e iso-8859-1 -file True -process 8 -dt sp_iptu -s 2 -encrypt 256 /home/thiagonobrega/zexp/odata/SP_Adresses/parsed_iptu.csv |&  tee sp_iptu.log

echo "FEII"
time python3 calculate_Signatures.py -file True -process 8 -dt feii_lei -s 2 -encrypt 256 /home/thiagonobrega/zexp/odata/feii/parsed_lei.csv |&  tee feii_lei.log
time python3 calculate_Signatures.py -file True -process 8 -dt feii_sec -s 2 -encrypt 256 /home/thiagonobrega/zexp/odata/feii/parsed_sec.csv |&  tee feii_sec.log

echo "DRUGS"
time python3 calculate_Signatures.py -file True -process 8 -dt drugs_fda -s 4 -encrypt 1024 /home/thiago/dados/drugs/drugsfda.csv |& tee drugs_fda.log
time python3 calculate_Signatures.py -file True -process 8 -dt drugs_ca -s 4 -encrypt 1024 /home/thiago/dados/drugs/drugsca.csv |& tee drugs_ca.log
#time python3 calculate_Signatures.py -file True -process 8 -dt drugs_fda -s 2 -encrypt 1024 /home/thiagonobrega/zexp/odata/drugs/drugs_fda.csv |& tee drugs_fda.log
#time python3 calculate_Signatures.py -file True -process 8 -dt drugs_ca -s 2 -encrypt 1024 /home/thiagonobrega/zexp/odata/drugs/drugs_ca.csv |& tee drugs_ca.log

echo "PE"
time python3 calculate_Signatures.py -file True -process 8 -dt pe_mpog -s 2 -encrypt 256 /home/thiagonobrega/zexp/odata/PublicEmployees/mpog.csv |&  tee pe_mpgo.log
time python3 calculate_Signatures.py -file True -process 8 -dt pe_tce -s 2 -encrypt 256 /home/thiagonobrega/zexp/odata/PublicEmployees/tce.csv |& tee pe_tce.log

echo "REST"
time python3 calculate_Signatures.py -file True -dt rest_tripadvisor -s 2 -process 8 -encrypt 2048 /home/thiagonobrega/zexp/odata/Restaurants/tripadvisor_data.csv |& tee log_trip.txt
time python3 calculate_Signatures.py -file True -dt rest_yelp -s 2 -process 8 -encrypt 2048 /home/thiagonobrega/zexp/odata/Restaurants/yelp_data.csv |& tee log_yelp.txt

#time python3 calculate_Signatures.py -dt voters_nc -s 1 -process 4 -encrypt 32512 /home/thiago/exp/DataSetUtil/samples/ncvoter/ |& tee log_ncvoters.txt
#time python3 calculate_Signatures.py -dt voters_ohio -s 1 -process 4 -encrypt 2048 /home/thiago/exp/DataSetUtil/samples/ohiovoters/ |& tee log_ohiovoters.txt

#time python3 calculate_Signatures.py -dt abt_g -s 1 -encrypt 2048 /home/thiago/exp/data/gregos/abt/ | tee log_abt.txt
#time python3 calculate_Signatures.py -dt buy_g -s 1 -encrypt 2048 /home/thiago/exp/data/gregos/buy/ | tee log_.txt
#time python3 calculate_Signatures.py -dt amazon_g -s 1 -encrypt 32512 /home/thiago/exp/data/gregos/amazon/ | tee log_.txt
#time python3 calculate_Signatures.py -dt dblp_g -s 1 -encrypt 2048 /home/thiago/exp/data/gregos/dblp/ | tee log_.txt
#time python3 calculate_Signatures.py -dt acm_g -s 1 -encrypt 2048 /home/thiago/exp/data/gregos/acm/ | tee log_.txt
#time python3 calculate_Signatures.py -dt google_g -e iso-8859-1 -s 1 -encrypt 32512 /home/thiago/exp/data/gregos/google/ | tee log_.txt
#time python3 calculate_Signatures.py -dt scholar_g -e iso-8859-1 -s 1 -encrypt 2048 /home/thiago/exp/data/gregos/scholar/ | tee log_scholar.txt
#time python3 calculate_Signatures.py -dt imdb_g -s 1 -encrypt 32512 /home/thiago/exp/data/gregos/imdb/ | tee log_imdb.txt
#time python3 calculate_Signatures.py -dt dbpedia_g -s 1 -encrypt 32512 /home/thiago/exp/data/gregos/dbpedia/ | tee log_dbpedia.txt
#time python3 calculate_Signatures.py -dt imdb_g -s 1 -encrypt 128 /home/thiago/exp/data/gregos/imdb/ | tee log_imdb.txt
#time python3 calculate_Signatures.py -dt dbpedia_g -s 1 -encrypt 128 /home/thiago/exp/data/gregos/dbpedia/ | tee log_dbpedia.txt

echo "PE"
time python3 calculate_Signatures.py -file True -process 8 -dt pe_mpog -s 2 -encrypt 2048 /home/thiago/dados/PublicEmployees/mpog.csv |&  tee pe_mpgo.log
time python3 calculate_Signatures.py -file True -process 8 -dt pe_tce -s 2 -encrypt 256 /home/thiago/dados/PublicEmployees/tce.csv |& tee pe_tce.log

echo "REST"
time python3 calculate_Signatures.py -file True -dt rest_tripadvisor -s 2 -process 8 -encrypt 2048 /home/thiago/dados/Restaurants/tripadvisor_data.csv |& tee log_trip.log
time python3 calculate_Signatures.py -file True -dt rest_yelp -s 2 -process 8 -encrypt 2048 /home/thiago/dados/Restaurants/yelp_data.csv |& tee log_yelp.log

echo "US_VOTERS"
time python3 calculate_Signatures.py -file True -dt voters_nc -s 4 -process 8 -encrypt 1024 /home/thiago/dados/us_voters/ncvoter.csv |& tee log_ncvoters.log
time python3 calculate_Signatures.py -file True -dt voters_ohio -s 4 -process 8 -encrypt 1024 /home/thiago/dados/us_voters/ohio_voters.csv |& tee log_ohiovoters.log

######
echo "US_VOTERS"
time python3 calculate_Signatures.py -file True -dt voters_nc -s 4 -process 8 -encrypt 1024 /home/thiago/dados/us_voters/ncvoter.csv |& tee log_full_ncvoters.log
time python3 calculate_Signatures.py -file True -dt voters_ohio -s 4 -process 8 -encrypt 1024 /home/thiago/dados/us_voters/ohio_voters.csv |& tee log_ohiovoters.log

echo "FEII"
time python3 calculate_Signatures.py -file True -process 8 -dt feii_lei -s 2 -encrypt 256 /home/thiagonobrega/zexp/odata/feii/parsed_lei.csv |&  tee log_ful_feii_lei.log
time python3 calculate_Signatures.py -file True -process 8 -dt feii_sec -s 2 -encrypt 256 /home/thiagonobrega/zexp/odata/feii/parsed_sec.csv |&  tee log_ful_feii_sec.log

echo "SP"
time python3 calculate_Signatures.py -file True -process 4 -dt sp_cnefe -s 2 -encrypt 256 /home/thiago/dados/SP_Adresses/parsedcnef.csv |&  tee log_ful_sp_cnefe.log
time python3 calculate_Signatures.py -e iso-8859-1 -file True -process 4 -dt sp_iptu -s 2 -encrypt 256 /home/thiago/dados/SP_Adresses/parsediptu.csv |&  tee log_ful_sp_iptu.log
#time python3 calculate_Signatures.py -file True -process 4 -dt sp_iptu -s 2 -encrypt 256 /home/thiago/dados/SP_Adresses/parsediptu.csv |&  tee log_ful_sp_iptu.log

echo "DRUGS"
time python3 calculate_Signatures.py -file True -process 4 -dt drugs_fda -s 4 -encrypt 1024 /home/thiago/dados/drugs/drugsfda.csv |& tee log_ful_drugs_fda.log
time python3 calculate_Signatures.py -file True -process 4 -dt drugs_ca -s 4 -encrypt 1024 /home/thiago/dados/drugs/drugsca.csv |& tee log_ful_drugs_ca.log

echo "PE"
time python3 calculate_Signatures.py -file True -process 8 -dt pe_mpog -s 2 -encrypt 256 /home/thiago/dados/PublicEmployees/mpog.csv |&  tee log_ful_pe_mpgo.log
time python3 calculate_Signatures.py -file True -process 8 -dt pe_tce -s 2 -encrypt 256 /home/thiago/dados/PublicEmployees/tce.csv |& tee log_ful_pe_tce.log

echo "REST"
time python3 calculate_Signatures.py -file True -dt rest_tripadvisor -s 2 -process 8 -encrypt 2048 /home/thiago/dados/Restaurants/tripadvisor_data.csv |& tee log_ful_log_trip.log
time python3 calculate_Signatures.py -file True -dt rest_yelp -s 2 -process 8 -encrypt 2048 /home/thiago/dados/Restaurants/yelp_data.csv |& tee log_ful_log_yelp.log
