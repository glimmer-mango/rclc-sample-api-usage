import os
import requests

API_KEY = os.getenv("API_KEY", "my-api-key")
API_URL = 'http://localhost:8000'

def main():
    # pass api key in header
    headers = {'api_key': API_KEY}
    print("Using API key", API_KEY)

    # upload a training dataset
    with open('./data/lymph-train-100.zip', 'rb') as fdata:
        files = {'data': fdata}
        params = {'name': 'lymph-train-100-final'} # change to your desired dataset name
        print("Please wait while your dataset is being uploaded to the API...")
        r = requests.post(f"{API_URL}/datasets", headers=headers, files=files, params=params)
        data_train = r.json()
        print("Upload is complete. Dataset id is", data_train)

    # train a new model
    print("Starting new model training session...")
    r = requests.post(f"{API_URL}/models", headers=headers, json={
        'dataset_id': data_train['dataset_id'],
        'strategy': 'new',
        'name': '3rd time charm', # change to your desired model name
        'test_size': 0.1,
        'eval_type': 'naive-bayes',
        'channel_pick': 'combine',
        'rcl_ticks': 10,
    })
    print("Check your dashboard to get the new model id")

    # Check your dashboard to get the new model id

if __name__ == '__main__':
    main()
