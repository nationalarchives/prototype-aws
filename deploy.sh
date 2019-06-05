zip tdr-run-tasks.zip tdr/runtasks.py
aws s3 cp tdr-run-tasks.zip s3://tdr-run-tasks
aws lambda update-function-code --function-name tdr-run-tasks --s3-bucket tdr-run-tasks --s3-key tdr-run-tasks.zip
