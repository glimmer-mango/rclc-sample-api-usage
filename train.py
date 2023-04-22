import os
import requests

API_KEY = os.getenv("API_KEY", "my-api-key")
API_URL = 'https://rclc.api.com'

def main():
    # upload a training dataset
    with open('path-to-my-data.zip', 'rb') as fdata:
        files = {'upload_file': fdata}
        values = {'name': 'my fancy dataset name'}
        r = requests.post(f"{API_URL}/datasets", files=files, data=values)
        data_train = r.json()

    # train a new model
    r = requests.post(f"{API_URL}/models", json={
        'dataset_id': data_train['id'],
        'strategy': 'new',
        'name': 'string',
        'test_size': 0.1,
        'eval_type': 'naive-bayes',
        'channel_pick': 'combine',
        'rcl_ticks': 10,
    })

    # TODO: get a model from job id
    job = r.json()

    # upload a test dataset
    with open('path-to-my-test-data.zip', 'rb') as fdata:
        files = {'upload_file': fdata}
        values = {'name': 'my fancy test dataset name'}
        r = requests.post(f"{API_URL}/datasets", files=files, data=values)
        data_test = r.json()

    # test your new model
    r = requests.post(f"{API_URL}/inferences", json={
        'dataset_id': data_test['id'],
        # TODO: get model_id
        'model_id': model_id,
    })

    # TODO: download .zip results file
    # get the results
    r = requests.get(f"{API_URL}/results/{test_job_id}")
    with open('path-to-zip-file', 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)



if __name__ == '__main__':
    main()
