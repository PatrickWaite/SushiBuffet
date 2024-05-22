# SushiBuffet
this project is meant to facilitate collecting and processing Counter 5 usage data using the SUSHI API across multiple independent vendors. 

## Setup of SushiBuffet
to start using the SushiBuffet script 
1. download the git repository
2. open vendorTemplate.json 
3. "Save As" or rename as vendor.json (or replace 'vendor.json' on line 119 in sushiBuffet.py with 'vendorTemplate.json')
4. open 'vendor.json' and enter in your vendor name, Requestor_id, customer_id, and api_key if applicable, this will give the program information to build the call string when its run.
5. save your vendor.json document
6. in sushiBuffet.py file lines 114, 115, and 116 represent the report type your calling for, the report start date and the report end date. adjust this in accordance with what report and period you are looking for. 
7. save sushiBuffet.py file
8. run sushiBuffet.py as you would (either in IED or as a CLI)
