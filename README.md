# cox_auto_programming_challenge
Code for Cox Auto programming challenge.

## Docker image build instructions 
From the directory containing the Dockerfile:

```Bash
docker build -t cox_auto_app:0.0.1 .
```

## Docker image run instructions to execute wpe_merge executable
Running from the location containing which contains the `data`
directory. The `data` directory contains the input .csv file(s).
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

### Run test unit tests
```Bash
docker run --rm --entrypoint pytest cox_auto_app:0.0.1 ./tests/test_test.py
```
