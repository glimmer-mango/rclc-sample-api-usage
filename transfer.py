import os
import pprint
import re
import requests
import time

# VARIABLES
API_KEY = os.getenv("API_KEY", "my-api-key")
API_URL = 'http://localhost:8000'
BASE_MODEL_ID = '<YOUR_EXISTING_MODEL_ID>' # check your dashboard to see model ids
DATASET_NAME = 'my-dataset-name'
TRANSFER_MODEL_NAME = 'my-transfer-model-name' # name for your new transfer model
TEST_SIZE = 0.1 # splits data into a test set. Set to 0 to train only with no test.
TRAINING_DATASET_PATH = '<PATH_TO_YOUR_DATASET_ZIP>' # make sure dataset is a zip file
WAIT_TIME = 5 # polling interval in seconds to check transfer learning model training status

def main():
    # pass api key in header
    headers = {'api_key': API_KEY}
    print("Using API key", API_KEY)

    # upload a training dataset
    with open(TRAINING_DATASET_PATH, 'rb') as fdata: 
        files = {'data': fdata}
        params = {'name': DATASET_NAME} 
        print("Please wait while your dataset is being uploaded to the API...")
        r = requests.post(f"{API_URL}/datasets", headers=headers, files=files, params=params)
        data_train = r.json()
        print("Upload is complete. Dataset id is", data_train['dataset_id'])

    # transfer learning
    # specifies an existing model to be augmented by additional training on new data of similar shape
    print("Starting transfer learning model training session...")
    r = requests.post(f"{API_URL}/models", headers=headers, json={
        'base_model_id': BASE_MODEL_ID,
        'dataset_id': data_train['dataset_id'],
        'strategy': 'transfer',
        'name': TRANSFER_MODEL_NAME,
        'test_size': TEST_SIZE,
        'eval_type': 'naive-bayes',
        'channel_pick': 'combine',
        'rcl_ticks': 10,
    })
    job_id = r.json()['job_id']
    print("Please wait until transfer learning session with job id", job_id, "has finished...")

    # wait until transfer learning model training is complete
    print("Continuously polling to get transfer learning status...")
    pp = pprint.PrettyPrinter(indent=4)
    while True:
        r = requests.get(f"{API_URL}/jobs/{job_id}", headers=headers)
        if (r.json()['status'] == 'finished'):
            print("Transfer learning model training is complete! Check your dashboard to get the new model id.")
            break
        print("Model training status on", re.sub(r'[^A-Z\d\:\-\s]', '', time.strftime('%Y-%m-%dT%H:%M:%S %p - %Z')))
        pp.pprint(r.json())
        time.sleep(WAIT_TIME)

    # Check your dashboard to get the new model id

if __name__ == '__main__':
    main()
