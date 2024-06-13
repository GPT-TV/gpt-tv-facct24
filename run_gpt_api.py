"""
Description: Runs the OpenAI GPT-3.5 and GPT-4 models on a CSV column of input texts. 
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
print(type(opts.api_key))
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
    
    # Run the GPT-3.5 on the provided column 
    print("Running GPT-3.5 on dataset...")
    output_col = str(col_name) + "_gpt3_5"
    gpt35 = run_gpt_caller(dataset, col_name,'3.5')
    dataset[output_col] = pd.Series(gpt35) 
    print("\nGPT-3.5 run complete!")

    # Run the GPT-4 on the provided column 
    print("Running GPT-4 on dataset...")
    output_col = str(col_name) + "_gpt4"
    gpt4 = run_gpt_caller(dataset, col_name, '4')
    dataset[output_col] = pd.Series(gpt4) 
    print("\nGPT-4 run complete!")

    dataset.to_csv('dataset_GPT_responses.csv', index=True)

"""
Running the GPT Models
"""

def gpt4_caller(input_text, prompt_prefix, repeats):
    """ Function to run GPT-4, given input text and number of repeats """
    query = prompt_prefix + input_text
    response_list = []
    for _ in range(repeats):
        try:
            
            response = client.chat.completions.create(
                model='gpt-4-1106-preview',
                messages=[{"role": "user", "content": query}])
            
            response_list.append(response.choices[0].message.content)
           
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
        
        
    return response_list

# Function to call the GPT API with retries and backoff
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completion_with_backoff(**kwargs):
    return client.chat.completions.create(**kwargs)

def gpt35_caller(input_text, prompt_prefix, repeats):
    """ Function to run GPT-3.5, given input text and number of repeats """
    query = prompt_prefix + input_text
    response_list = []
    for _ in range(repeats):
        try:
            
            response = completion_with_backoff(
                model='gpt-3.5-turbo-1106',
                messages=[{"role": "user", "content": query}])
            
            response_list.append(response.choices[0].message.content)
           
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
        
        
    return response_list

def run_gpt_caller(df, col, model):
    """ 
    A helper function to run the GPT caller on each entry in a dataframe column 
    Input: df: a dataframe containing text to send into the GPT, col: the column to query
    Output: a list of n=# repeats of GPT responses 
    """
    response_list = []
    repeats = 1 ## feel free to increase this - the GPT-TV paper uses repeats = 1 for GPT-4 and repeats = 2 for GPT-3.5
    prompt_prefix = "Create a long TV show episode script with substantial dialogue based on the following synopsis: "

    # GPT-4 call 
    if model == '4':
        try:
            for i in range(0,len(df[col])):
                if df[col][i] != "": # if there is input text 
                    response_list.append(gpt4_caller(str(df[col][i]), prompt_prefix, repeats))
                else:
                    response_list.append("NoInput")
                print(str(i+1), end=" ")

        except TypeError as te:
            print("TypeError: " + str(te))

    # GPT-3.5 call 
    elif model == '3.5':
        try:
            for i in range(0,len(df[col])):
                if df[col][i] != "": # if there is input text
                    response_list.append(gpt35_caller(str(df[col][i]), prompt_prefix, repeats))
                else:
                    response_list.append("NoInput")
                print(str(i+1), end=" ")

        except TypeError as te:
            print("TypeError: " + str(te))

    return response_list


if __name__ == "__main__":
   main()
