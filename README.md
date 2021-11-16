# bootleg-ebay
Topics in Software Engineering Course Project.... Creating a Bootleg Ebay


Test commit


# Some notes

* Try to do type hinting for all interface functions. You don't need to have type hinting for non-interface functions.


# Testing
## Running tests

We can put the tests within each microservice directory.

Run something like:

```
cd tests/

# to run all tests
python -m unittest discover -v

# to run one file
python -m unittest test_user
```

## Writing Tests

A few things to note for writing tests for mediator:

* Make sure that all the tests run correctly before merging your branch with main. Or else someone else may have to debug the code that you write, which is much harder for the other person than it is for you
    * Also, the point of the tests is to ensure that nothing breaks
    * In real world software, the code manager is going to reject your code if it doesn't pass all the tests
* Your tests should not assume the existence of objects. Create those objects if you need to and then delete them afterwards