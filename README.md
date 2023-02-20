# miRNA-Disease Association Lookup Tool

Overview

This is a command-line tool for analysing miRNA and disease data. The tool accepts a CSV file as input and provides a filtered dataframe based on the optional parameters of miRNA name, disease name, and confidence scores. The tool also provides error messages if the inputs are not found in the data or confidence scores are outside the expected range. Using the defined function wrap_cell(), the 'Disease' column values are wrapped to a width of 35 characters to fit the display.

Usage

The script can be run from the command line with the following parameters:

python script_name.py -f <file_name> -m <mirna_name> -d <disease_name> -s <Confidence_score1> -c < Confidence_score2>

Input Parameters

file_name (required): The name of the csv file that you want to read. The file should contain columns 'miRNA', 'Gene', 'Confidence_score1', 'Disease', 'Confidence_score2'.
mirna (optional): The name of the miRNA you want to search for in the data. The default value is an empty string.
disease (optional): The name of the disease you want to search for in the data. The default value is an empty string.
score1 (optional): The minimum Confidence_score1 value required to return a row. The default value is 80.
score2 (optional): The minimum Confidence_score2 value required to return a row. The default value is 0.8.
Output

The function returns a pandas dataframe containing the rows that match the input conditions. The dataframe has columns 'miRNA', 'Gene', 'Confidence_score1', 'Disease', 'Confidence_score2', and 'Number'. The 'Number' column is an index that starts from 1 to the length of the result data.

If there are no rows that match the input conditions, the tool returns an empty dataframe. If the inputs are not found in the data or are outside the expected range, the tool returns warning messages.

Examples

Example 1: To search for a miRNA 'hsa-miR-17-5p' and a disease 'cancer' in the file 'data.csv', using the default values for confidence scores:

python lookup.py -f data.csv -m 'hsa-miR-17-5p' -d 'cancer'

Example 2: To search for a miRNA 'hsa-miR-17-5p' in the file 'data.csv', using a confidence score1 of 85 and the default value for confidence score2.

python lookup.py -f data.csv -m 'hsa-miR-17-5p' -s 85

Example3: To search for a disease 'cancer' in the file 'data.csv', using a confidence score2 of 0.9 and the default values for miRNA and score1.

python lookup.py -f data.csv -d 'cancer' -c 0.9

Example4: To search for miRNA 'hsa-miR-17-5p' and disease 'cancer' in the file 'data.csv', using confidence scores of 95 for score1 and 0.85 for score2.

python lookup.py -f data.csv -m 'hsa-miR-17-5p' -d 'cancer' -s 95 -c 0.85

Example5: To search for all entries in the file 'data.csv', using the default values for miRNA, disease, score1, and score2.

python lookup.py -f data.csv

Error Handling

If the file specified in file_name is not found, the function returns an error message "Error: The file [file_name] does not exist."
If the values of score1 and score2 are not within the range of 80 to 100 and 0.8 to 1, respectively, a warning message "Note: Confidence values are not within the range." is printed.
If the input miRNA and disease names are not found in the data, a warning message "Note: Inputs '[mirna]' and '[disease]' for both miRNA and Disease names have mistakes or not found in the dataset." is printed.
If only the input miRNA name is not found in the data, a warning message "Note: No data for the miRNA input '[mirna]' was found. However, data for the '[disease]' entry was found in the dataset." is printed.
If only the input disease name is not found in the data, a warning message "Note: There is an error in the disease name you entered but data for the '[mirna]' was found in the file." is printed.
