#!/bin/bash
# deployment
#export PYTHONPATH=/root/forecast_deployment/landuseregression/datapre/src:/root/forecast_deployment/landuseregression/datapre-tools/src:/root/forecast_deployment/landuseregression/model/src
#python3.4 /root/forecast_deployment/landuseregression/forecast/src_python/forecast.py /root/forecast_deployment/
#rm /media/storage/forecast/data/*
#cp /root/forecast_deployment/output/* /media/storage/forecast/data/

# test
export PYTHONPATH=/home/makrai/git/landuseregression/datapre/src:/home/makrai/git/landuseregression/datapre-tools/src:/home/makrai/git/landuseregression/model/src
python3.4 /home/makrai/Documents/"LiClipse Workspace"/forecast/src_python/forecast.py
#rm /media/storage/forecast_test/data/*
#cp /media/sf_lur/forecast/output/* /media/storage/forecast_test/data/
