import argparse
import textwrap

# function to wrap cell contents
def wrap_cell(text, width):
    wrapped = textwrap.wrap(text, width=width)
    return "\n".join(wrapped)

def lookup(file_name, mirna='', disease='', score1=80, score2=0.8):
    """
    This function takes a file_name and optionally, mirna name, disease name, score1 and score2 as input.
    and returns a dataframe containing rows matching the input conditions.
    """
    import pandas as pd

    # Try reading the csv file
    try:
        data = pd.read_csv(file_name)
    except FileNotFoundError:
        print(f"\033[1;31mError: The file {file_name} does not exist.\033[0m")
        return

    # Try converting score1 and score2 to float, if unsuccessful, set default values
    try:
        score1 = float(score1)
    except ValueError:
        score1 = 80
    try:
        score2 = float(score2)
    except ValueError:
        score2 = 0.8

    # convert mirna and disease names to lowercase
    mirna = mirna.lower()
    disease = disease.lower()

    check1 = data['miRNA'].str.contains(mirna)          # Check if mirna name is present in the data
    check2 = data['Disease'].str.contains(disease)      # Check if disease name is present in the data


    # If score1 and score2 are not within the expected range, print a warning message
    if (((score1 >= 80 and score1 <= 100) ==False) or ((score2 >= 0.8 and score2 <= 1)) == False):
        print(170*'-')
        print("\033[1;31mNote: Confidence values are not within the range.\033[0m")

    # If mirna and disease names are not found in the data, print a warning message
    if (not check1.any()) and (not check2.any()):
        print(170*'-')
        m =f"\033[1;31mNote: Inputs '{mirna}' and '{disease}' for both miRNA and Disease names have mistakes or not found in the dataset.\033[0m"
        print(m)
        print((len(m)-11)*'-')
        return
    
    # If only mirna name is not found in the data, print a warning message
    if (not check1.any()):
        print(170*'-')
        m = f"\033[1;31mNote: No data for the miRNA input '{mirna}' was found. However, data for the '{disease}' entry was found in the dataset.\033[0m"
        print(m, f"\n\033[1;31mIf no disease name was given, all data in the given file is printed.\033[0m")
        print((len(m)-11)*'-')
        mirna = 'hsa'

    # Check if the disease name input is not found in the data, print a warning message
    if (not check2.any()):
        print(170*'-')
        m = f"\033[1;31mNote: There is an error in the disease name you entered but data for the '{mirna}' was found in the file.\033[0m"
        print(m)
        print((len(m)-11)*'-')
        disease = ''

        

    result = data.loc[(data['miRNA'].str.contains(mirna)) & (data['Disease'].str.contains(disease)) & (data['Confidence_score1'] >= score1) & (data['Confidence_score2'] >= score2)]           # Filter the data to get only the rows that contain the input mirna and disease name and match the confidence scores
    result = result[['miRNA', 'Confidence_score1', 'Gene', 'Disease', 'Confidence_score2']].drop_duplicates(subset=['miRNA', 'Gene', 'Disease'], keep='first')          # Remove duplicates while keeping the first occurrence and only keeping the desired columns
    result['Disease'] = result['Disease'].apply(lambda x: x.capitalize())
    result['Disease'] = result['Disease'].apply(lambda x: wrap_cell(x, 35))          # Wrap the values in the 'Disease' column to a width of 35 characters
    result['Number'] = range(1, len(result)+1)            # Add a column 'Number' with a range of values starting from 1 to the length of the result data
    result = result.set_index('Number')          # Set the 'Number' column as the index of the result data
    
    # Check if the length of the result data is greater than 0
    if len(result) > 0:
        return(result)
    else:
        return None         # Return None if there is no result data


# Create argument parser object
parser = argparse.ArgumentParser(description="miRNA-Disease association Lookup tool")

# Add arguments for file name, miRNA name, disease name, miRNA/locus confidence score, and gene/disease confidence score
parser.add_argument('-f', '--file_name', type=str, metavar='', required=True, help='File name containing the dataset.')
parser.add_argument('-m', '--mirna', type=str, metavar='', default = '', required=False, help='miRNA name or part of the name.')
parser.add_argument('-d', '--disease', type=str, metavar='', default = '', required=False, help="Disease name or part of the name.")
parser.add_argument('-s', '--score1', type=str, metavar='', default = 80, required=False, help="miRNA/locus confidence score. It should be within the range (80-100), otherwise no results will be printed.")
parser.add_argument('-c', '--score2', type=str, metavar='', default = 0.8, required=False, help="gene/disease  confidence score. It should be within the range (0.8-1), other than that no results will be printed.")


# Add mutually exclusive group for with_scores argument
group = parser.add_mutually_exclusive_group()
group.add_argument('-with', '--with_scores', action='store_true', help="For printing data with the relevant 'miRNA/locus' and 'gene/disease' confidence scores." )
args = parser.parse_args()


if __name__ == '__main__':
    result = lookup(args.file_name, args.mirna, args.disease, args.score1, args.score2)

    # Print user inputs
    print("\033[1;33mYour Inputs:\033[0m")
    print(f"\033[1;36mmiRNA:\033[0m", f"\033[36m{args.mirna}\033[0m")
    print(f"\033[1;36mDisease Name:\033[0m", f"\033[36m{args.disease}\033[0m")
    print(f"\033[1;36mmiRNA/locus confidence score:\033[0m", f"\033[36m{args.score1}\033[0m")
    print(f"\033[1;36mgene/disease confidence score:\033[0m", f"\033[36m{args.score2}\033[0m")
    print(35*'-')
    
    
    # Check if result is not None
    if result is not None:

        # Check if with_scores argument is True
        if args.with_scores:
            result = result[['miRNA', 'Confidence_score1', 'Gene', 'Disease', 'Confidence_score2']]         # Filter result to only include relevant columns with confidence scores
            print("\033[32mData reported with confidence scores.\033[0m")
            print(37*'-')

        else:
            result = result[['miRNA', 'Gene', 'Disease']]
            print("\033[32mData reported without confidence scores.\033[0m")
            print(40*'-')
        print(result.to_markdown())         # Print result in markdown format

    else:
        print("\033[3;32mNo results were found for your search criteria. Try changing confidence score values or the inputs for the file, miRNA or disease names.\033[0m")
        print(136*'-')
