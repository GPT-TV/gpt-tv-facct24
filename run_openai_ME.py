"""
Description: Runs the OpenAI moderation endpoint (ME) on a CSV column of input texts. 
Authors: Charlie Crawford and Yaaseen Mahomed
Created for use in the GPT-TV audit pipeline, more information here: https://github.com/GPT-TV/gpt-tv-facct24
"""

# Imports:
import pandas as pd
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential
import openai
import util


"""
Creating the OpenAI API Client
"""
opts = util.parse_args()
client = OpenAI( 
  api_key = opts.api_key  # Using provided API key, instantiate OpenAI client object 
)

"""
Reading in Data
"""
def main():
    
    col_name = opts.col_name

    # Check for valid dataset and column inputs 
    try:
        dataset = pd.read_csv(opts.dataset_filename)
    except: 
       print("Dataset file not found. Check that your file is in CSV format and spelled correctly!")
       return
    try:
       dataset[col_name]
    except:
       print("Unable to find column named \'" + col_name + "\' in dataset!")
       return
  
    # Run the ME on the provided column 
    print("Running ME on dataset...")
    output_col = str(col_name) + "_ME_response"
    ME_response = run_me_caller(dataset, col_name) # optionally, change # of repeats with reps=# 
    dataset[output_col] = pd.Series(ME_response)
    print("ME run complete!")

    dataset.to_csv('dataset_ME_responses.csv', index=False)


"""
Running the Moderation Endpoint
"""

def me_caller(input_text, repeats): 
    """ Function to run the ME, given input text and number of repeats """
    response_list = []
    for _ in range(repeats):
        try:
            response = client.moderations.create(input=input_text)
            response_list.append(response.results[0])
        except openai.APIError as e:
          #Handle API error here, e.g. retry or log
          print(f"OpenAI API returned an API Error: {e}")
          response_list.append("API Error Response")
        except openai.APIConnectionError as e:
          #Handle connection error here
          print(f"Failed to connect to OpenAI API: {e}")
          response_list.append("API Error Response")
        except openai.RateLimitError as e:
          #Handle rate limit error (we recommend using exponential backoff)
          print(f"OpenAI API request exceeded rate limit: {e}")
          response_list.append("API Error Response")
        except openai.Timeout as e:
          #Handle API error here, e.g. retry or log
          print(f"OpenAI API returned an API Error: {e}")
          response_list.append("API Error Response")
        except openai.InvalidRequestError as e:
          #Handle connection error here
          print(f"Failed to connect to OpenAI API: {e}")
          response_list.append("API Error Response")
        except openai.AuthenticationError as e:
          #Handle rate limit error (we recommend using exponential backoff)
          print(f"OpenAI API request exceeded rate limit: {e}")
          response_list.append("API Error Response")
        except openai.ServiceUnavailableError as e:
          #Handle rate limit error (we recommend using exponential backoff)
          print(f"OpenAI API request exceeded rate limit: {e}")
          response_list.append("API Error Response")
        except Exception as e:
            # Handle other exceptions
            print(f"An unexpected error occurred: {e}")
            response_list.append("Unexpected Error Response")
    return response_list



def run_me_caller(df, col, reps=20):
    """ 
    A helper function to run the ME caller on each entry in a dataframe column 
    Input: df: a dataframe containing text to send into the ME, col: the column to query
    Output: a list of n=# repeats of ME responses 
    """
    response_list = []
    repeats = reps ## feel free to increase this, default is 20

    try:
        for i in range(0,len(df[col])):
            if type(df[col][i]) == str and df[col][i] != "" and df[col][i] != "NoInput": # if there is a GPT script 
                response_list.append(me_caller(df[col][i], repeats))
            else:
                response_list.append("NoInput")
            print(str(i+1), end=" ")

    except TypeError as te:
        print("TypeError: " + str(te))
    pass

    return response_list


if __name__ == "__main__":
   main()
