# Mocking and Patching

## Installation and Set Up
1. You will need **at least** Python 3.10.6.
2. Fork and clone the repository. 
3. Create a virtual environment.
4. Activate the environment and run `pip install -r requirements.txt`
5. Ensure that you can access the `cruncher` classes in the REPL as shown in the example below.

## Troubleshooting Pytest

It's quite common to see the following error when first setting up this sprint: 
```
ModuleNotFoundError: No module named 'requests'
```
Here are a few steps you can take:
- Deactivate your Virtual Environment, delete your `venv` folder and follow the setup steps again to recreate it and install the requirements.
- Close you terminal session and reopen it. Set the `PYTHONPATH` environment variable and try running `pytest` again.
- When you're inside the Virtual Environment check where the `pytest` command is located. You can do this by running the command `which pytest`. It should give you the path to your local Venv directory. 
- If the `pytest` command is not located in your local Venv then you may have installed Python globally on your machine. If that is the case then deactivate your venv and uninstall the global `pytest` by running `pip uninstall pytest`. Reactivate your virtual environment and re-run the `pytest` command.

If this doesn't help then drop an NC Help and we'll help you get sorted!

<br>

## Sprint
The `cruncher.py` file contains two classes, `NumberRequester` and `NumberCruncher`. 

The `NumberRequester` gets a random number fact from the [numbersapi endpoint](http://numbersapi.com/). (Internally, it uses the `requests` API to make the REST call.) It makes a careful note of the results of each request in a log and returns a dictionary with the number and its associated fact.

### Example:
In the REPL:
```python
>>> from cruncher import NumberRequester
>>> nr = NumberRequester()
>>> nr.call()
{'result': 'SUCCESS', 'number': 473, 'fact': '473 is the largest known number whose square and 4^{th} power use different digits.'}
```

The `NumberCruncher` eats number facts, although it only has a limited capacity. When it is started you have to specify the size of its tummy (ie how many number facts it can store). It has a `NumberRequester` built in. To `crunch` a number, it uses the `NumberRequester` to get a number fact. It then does one of three things:
1. It hates odd numbers, so if the number is odd, it just rejects it with a "Yuk!" message.
2. If the number is even, and its tummy is not full, it happily eats the number fact and returns a "Yum!" message.
3. If the number is even, and its tummy is full, it expels the oldest number fact from its tummy to make room for the new one. It returns a "Burp!" message.

### Example:
If we start a REPL, we should be able to do something like this:
```python
>>> from cruncher import NumberCruncher
>>> nc = NumberCruncher(3) # a NumberCruncher that can store 3 facts
>>> nc.crunch()
'Yum! 8100'   # stored 8100. NumberRequester is invoked from within NumberCruncher
>>> nc.crunch()
'Yuk! 5335'
>>> nc.crunch()
'Yum! 730'  # stored
>>> nc.tummy()
[{'number': 8100, 'fact': '8100 is divisible by its reverse.'}, {'number': 730, 'fact': '730 is the number of connected bipartite graphs with 9 vertices.'}]
>>> nc.crunch()
'Yum! 436'  # stored - tummy full
>>> nc.crunch()
'Burp! 8100' # 8100 burped out to make room for the new fact
>>> nc.tummy()
[{'number': 730, 'fact': '730 is the number of connected bipartite graphs with 9 vertices.'}, {'number': 436, 'fact': '436 is a boring number.'}, {'number': 5624, 'fact': '5624 is the number of binary 5×5 matrices up to permutations of rows and columns.'}]
>>> nc.requester.log
[{'request_number': 1, 'call_time': '2022-11-09T16:38:23.417667', 'end_point': 'http://numbersapi.com/random/math', 'result': 'SUCCESS', 'number': 8100},  
{'request_number': 2, 'call_time': '2022-11-09T16:38:26.111704', 'end_point': 'http://numbersapi.com/random/math', 'result': 'SUCCESS', 'number': 5335},  
{'request_number': 3, 'call_time': '2022-11-09T16:38:37.810081', 'end_point': 'http://numbersapi.com/random/math', 'result': 'SUCCESS', 'number': 730},  
{'request_number': 4, 'call_time': '2022-11-09T16:38:55.040040', 'end_point': 'http://numbersapi.com/random/math', 'result': 'SUCCESS', 'number': 436},  
{'request_number': 5, 'call_time': '2022-11-09T16:39:07.712827', 'end_point': 'http://numbersapi.com/random/math', 'result': 'SUCCESS', 'number': 5624}]
```

So this works but - shock!!! - it has no unit tests!!! This is, of course, unacceptable. Your task is to write some. Two test files have been prepared with some specifications for behaviour we want to test for - one file tests `NumberCruncher` and one tests `NumberRequester`. However, the tests have not been implemented. You should implement them, making use of mocking techniques. 

### Task One - implement the tests in `test_cruncher.py`

### Task Two - implement the tests in `test_requester.py`

The code as written should pass the required tests. But if you complete those tests, feel free to write new ones making more rigorous checks on `NumberCruncher` and `NumberRequester` behaviour. If you think something is wrong, fix it!
