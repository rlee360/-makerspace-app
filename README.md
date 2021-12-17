# makerspace-app
A web-based print request system for Makerspaces

# Installation and Running Instructions

## Installing the backend manually

`mongodb` is needed on the testing system. 

It is recommended to use a python virtual environment such as `venv`

```bash
cd backend
sudo apt install python3-venv #install the venv package
python3 -m venv new_venv # create a venv titled 'new_venv'
source new_venv/bin/activate # enable the venv
pip install -r requirements.txt
python db/populate_db.py # establishes the database schemas and insers some sample documents
```
In order to run the backend, then run

```bash
python src/app.py
```
## Using docker to install and run the backend

The initial state of the database can be initialized with

The backend can be run following the instructions in `docker/README.md`

## Installing and running the frontend

The frontend can be installed by running `npm install` in the `makerspace-frontend` directory. The frontend can be started by running `npm run serve` in the `makerspace-frontend` directory.
