# cox_auto_programming_challenge
Code for Cox Auto programming challenge.

## Docker image build instructions 
From the directory containing the Dockerfile:
```Bash
docker build -t cox_auto_app:0.0.1 .
```

## Docker image run instructions to execute service executable
```Bash
docker run --rm cox_auto_app:0.0.1
```

## Docker image run instructions to execute tests
### Run all tests
```Bash
docker run --rm --entrypoint pytest cox_auto_app:0.0.1 ./tests/
```

### Run request tools unit tests
```Bash
docker run --rm --entrypoint pytest cox_auto_app:0.0.1 ./tests/request_tools_test.py
```

### Run data operations unit tests
```Bash
docker run --rm --entrypoint pytest cox_auto_app:0.0.1 ./tests/data_operations_test.py
```

### Run data collection unit tests
```Bash
docker run --rm --entrypoint pytest cox_auto_app:0.0.1 ./tests/data_collection_test.py
```
* Note: Currently doesn't implement tests for get_dealer_names and get_data_for_vehicles
        which implement threads.
