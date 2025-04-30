# Import libraries and other python files
import utils
import config
import  phonepedata

# Install the missing package
config.pkg_loader()
# Create and validate the Database
conn,cur= config.get_connection()
# Create the required table function
utils.table_creation()
# Clone the repository from GIT
utils.clone_repo()

#List of json file path
data_path_list = ['/data/data/aggregated/user/country/india/','/data/data/aggregated/transaction/country/india/',
                 '/data/data/aggregated/insurance/country/india/','/data/data/map/user/hover/country/india/',
                 '/data/data/map/transaction/hover/country/india/','/data/data/map/insurance/hover/country/india/',
                    '/data/data/top/user/country/india/','/data/data/top/transaction/country/india/',
                '/data/data/top/insurance/country/india/']

#Call the Json file path to transfer the record from JSON to SQL
for path in data_path_list:
    phonepedata.getjsonpath(path)
    phonepedata.sqlinsert(path)