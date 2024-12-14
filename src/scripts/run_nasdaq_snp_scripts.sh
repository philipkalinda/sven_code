#!/bin/bash

#-----------------------------------------------------------------------------------------------------------------------

script_start_s=$(date '+%s');
script_start_dt=$(date);

echo "Starting Scripts [Time: $script_start_dt]..."

#-----------------------------------------------------------------------------------------------------------------------

## Data Collection
cd ../data/
echo "Running Data Collection Protocols..."

#-----------------------------------------------------------------------------------------------------------------------

### NASDAQ
section_start_dt=$(date);
echo "Running NASDAQ Data Collection Protocol [$section_start_dt]..."

start_s=$(date '+%s');
python -m av_us_update_nasdaq_snp_databases
end_s=$(date '+%s');
let diff_s=$(echo "$end_s-$start_s" |bc)/60

echo "NASDAQ Data Collection Protocol Complete [Time Taken: $diff_s Minutes]..."

#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

## FEATURE GENERATION
cd ../features/
echo "Running Feature Generation Protocols..."


#-----------------------------------------------------------------------------------------------------------------------

### NASDAQ
section_start_dt=$(date);
echo "Running NASDAQ Feature Generation Protocol [section_start_dt]..."

start_s=$(date '+%s');
python -m ta_build_av_us_nasdaq_snp_features
end_s=$(date '+%s');
let diff_s=$(echo "$end_s-$start_s" |bc)/60

echo "NASDAQ Feature Generation Protocol Complete [Time Taken: $diff_s Minutes]..."


#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

## TECHNICAL ANALYSIS SIGNAL CHECKER
cd ../models/
echo "Running Technical Analysis Protocols..."

#-----------------------------------------------------------------------------------------------------------------------

section_start_dt=$(date);
echo "Running Technical Analysis Protocol [section_start_dt]..."

start_s=$(date '+%s');
python -m ta_update_technical_analysis
end_s=$(date '+%s');
let diff_s=$(echo "$end_s-$start_s" |bc)/60

echo "Technical Analysis Protocol Complete [Time Taken: $diff_s Minutes]..."


#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

script_end_s=$(date '+%s');
script_end_dt=$(date);
let script_diff_s=$(echo "$script_end_s-$script_start_s" |bc)/60


echo "All Protocols Complete [$script_end_dt]..."
echo "Time Taken: $script_diff_s Minutes"

#-----------------------------------------------------------------------------------------------------------------------

cd ../comms
python confirm_finish.py

