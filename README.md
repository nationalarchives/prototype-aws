# TDR AWS scripts

At the moment, this contains the lambda which receives the message from the s3 put event notification, sends this to an sqs queue and starts the containers to run the backend checks

## How to run tests locally

- Create a virtual environment

`python3 -m venv .`

- Activate the virtual environment

`source bin activate`

- Install dependencies

`pip install -r requirements.txt`

- Run tests

`python -B -m xmlrunner discover tests --output-file junit.xml`
