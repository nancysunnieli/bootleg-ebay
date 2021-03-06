# Bootleg Ebay

This is our Bootleg Ebay course project for the course MPCS 51205 (Topics in Software Engineering). The team members are Nancy Li, Yves Shum, and Jin Li.

# Description

Please see this [presentation](https://docs.google.com/presentation/d/11xmj2wEfghZHsrrXM-Mjprlc85pEcq2yGmSNwdGvGPA/edit?usp=sharing) for a description of our system.

# Running The Code

To run the code:

1. Change into the directory that contains the `docker-compose.yml` file.
2. Run `docker-compose up`. Please wait until all the services are up (this should take about a minute or two).
3. If this is your first time running the system, you need to load in data to the database. Please run:

```
cd data/
./importAllData.sh
```

4. After starting the system, go to `http://localhost:8000` to view the front end.

To shutdown the system:

1. Ctrl+C to stop the docker containers
2. Run `docker-compose down`

# Important Notes

## Admin

- An admin is basically a user with special priviledges. So that admin can create items and buy / bid on things.
- If an admin wants to suspend a user, he has to go to a specific auction and then click on the user name. There, he can suspend or unsuspend a user.

## Items / Auctions

- Reporting an item is the same as flagging an item
- Our system only allows for one auction to take place for each item at a given time
- When creating an item, the only format of photos that you are able to upload are PNGs


## Users

- If you want to have two users at the same time, you should open up an incognito tab.
- A suspended user cannot login.

## Other

- When inputing information into forms on the front end, make sure to fill in all the fields, otherwise the API will not allow you to move forward




# Testing

To run tests:

```
cd tests/

# to run all tests
python -m unittest discover -v

# to run one file
python -m unittest test_user
```

# Acknowledgements

Thank you to professor Mark Shacklette and the TAs Alan SalkanoviÄ‡ and John Hadidian-Bauger for their help and support.
