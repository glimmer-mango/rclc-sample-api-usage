import os
import pprint
import re
import requests
import time

# VARIABLES
ADD_MODEL_NAME = "my-add-model-name"
API_KEY = os.getenv("API_KEY", "my-api-key")
API_URL = "http://localhost:8000"
BASE_MODEL_ID = "<YOUR_EXISTING_MODEL_ID>"  # check your dashboard to see model ids
EXTRA_MODEL_IDS = [1, 2, 3]  # change this list to your extra model ids
TEST_SIZE = 0.1  # splits data into a test set. Set to 0 to train only with no test.
WAIT_TIME = 5  # polling interval in seconds to check add model training status


def main():
    # pass api key in header
    headers = {"api_key": API_KEY}
    print("Using API key", API_KEY)

    # add models
    # specifies a set of models to be added to a base model
    print("Starting add models training session...")
    r = requests.post(
        f"{API_URL}/models",
        headers=headers,
        json={
            "base_model_id": BASE_MODEL_ID,
            "extra_model_ids": EXTRA_MODEL_IDS,
            "strategy": "add",
            "name": ADD_MODEL_NAME,
            "test_size": TEST_SIZE,
            "eval_type": "naive-bayes",
            "channel_pick": "combine",
            "rcl_ticks": 10,
        },
    )
    job_id = r.json()["job_id"]
    print(
        "Please wait until add model training session with job id",
        job_id,
        "has finished...",
    )

    # wait until model training session is complete
    print("Continuously polling to get model training status...")
    pp = pprint.PrettyPrinter(indent=4)
    job = None
    while True:
        r = requests.get(f"{API_URL}/jobs/{job_id}", headers=headers)
        job = r.json()
        if job["status"] == "finished":
            print(
                "Add model training is complete! Check your dashboard to get the new model id."
            )
            break
        print(
            "Model training status on",
            re.sub(r"[^A-Z\d\:\-\s]", "", time.strftime("%Y-%m-%dT%H:%M:%S %p - %Z")),
        )
        pp.pprint(job)
        time.sleep(WAIT_TIME)

    # Write the results to a file
    r = requests.get(f"{API_URL}/results/{job['id']}", headers=headers)
    with open("/tmp/result.zip", "wb") as result_f:
        result_f.write(r.content)


if __name__ == "__main__":
    main()
