# Bootleg Ebay

This is our Bootleg Ebay course project for the course MPCS 51205 (Topics in Software Engineering). The team members are Nancy Li, Yves Shum, and Jin Li.

# Description

Please see this [presentation](https://docs.google.com/presentation/d/11xmj2wEfghZHsrrXM-Mjprlc85pEcq2yGmSNwdGvGPA/edit?usp=sharing) for a description of our system.

# Running The Code

To run the code:

1. Change into the directory that contains the `docker-compose.yml` file. 
2. Run `docker-compose up`


To shutdown the system:

1. Ctrl+C to stop the docker containers
2. Run `docker-compose down`


# Front end

After starting the system, go to `http://localhost:3000` to view the front end.


# Testing

To run tests:

```
cd tests/

# to run all tests
python -m unittest discover -v

# to run one file
python -m unittest test_user
```
