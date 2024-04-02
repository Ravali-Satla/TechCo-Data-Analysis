import sys
import getopt
import pandas as pd
from configparser import ConfigParser

#Read config.ini file
config_object = ConfigParser()
config_object.read("config.ini")


input_io = config_object["InputFile"]
output_op = config_object["OutputFile"]

def convert_csv_to_parquet(csv_file_path, parquet_file_path):
    # Read the CSV file into a pandas DataFrame
    csv_df = pd.read_csv(csv_file_path)

    # Write the pandas DataFrame to Parquet format
    csv_df.to_parquet(parquet_file_path, index=False)
    print('Conversion completed!')

def main(argv):
    inputfile = input_io
    outputfile = output_op
    
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
        
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
            
    print('Input file is', inputfile)
    print('Output file is', outputfile)
        
    # Call the conversion function
    convert_csv_to_parquet(inputfile, outputfile)

if __name__ == "__main__":
    main(sys.argv[1:])