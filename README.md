# SwAPI - Star Wars API cli tool

Simple command line tool used to get data from the [Star Wars API](https://swapi.dev/ "Main Page")
Written in Python 3.

### Table of Contents

- [SwAPI - Star Wars API cli tool](#swapi---star-wars-api-cli-tool)
    + [Installing](#installing)
    + [Usage](#usage)
        * [Search](#search)
        * [Get-planets](#get-planets)
    + [The Database](#the-database)
        * [Structure](#structure)
        * [Caching](#caching)
    + [Config](#config)
    
### Installing 
Clone the repository and make sure you installed all packages via Pip.
```bash
pip3 install -r requirements.txt
```
Creating an alias is recomended for easier usage:
```bash
alias swapi="python3 cli.py"
```
Make sure u have cluster of MongoDB up and running.
### Usage 
The usage is very simple, just run the command with python

```bash
usage: swapi [-h] {search,get-planets} ...

positional arguments:
  {search,get-planets}
    search              Search data in the StarWars API
    get-planets         Get data about all the planets from the API

optional arguments:
  -h, --help            show this help message and exit
```
There are 2 subcommands 
##### Search
Searches for data about spesific resource
```bash
usage: swapi search [-h] resource term

positional arguments:
  resource    The resource to serch in
  term        The term to search. For example: "R2-D2"

optional arguments:
  -h, --help  show this help message and exit
```
##### Get-planets
Getting all data about the planets. 
Data can be sorted.
```bash
usage: swapi get-planets [-h] field {dec,asc}

positional arguments:
  field       The field to order by
  {dec,asc}   The direction to sort the data

optional arguments:
  -h, --help  show this help message and exit
```

### The Database
I decided to use nosql type of database - **MongoDB**.
##### Structure
Inside the database there are serveral collections which are basicaly the resources from the API:
* films
* people
* planets
* starships
* species
* vehicles

Each collection holds unqiue data which is relavant to the spesific collection.
##### Caching
There is one special collection in the db called **cache**.

The collection holds records of the past insertions to the database. 
Each document has 2 fields, search_term and resource.

For example:
```json
{
    "search_term": "R2",
    "resource": "people"
}
```
The algorithm works in the following way:
Let's say somone already searched people with the search term "r".
By given that information we can be sure that all the results for "r2" must already be stored in the Database.

So, to check if some data is already cached in the Database all we need to do is to iterate over every contiguous substring in the search term and to check if one of them is already cached.

After validating the data was cached, we can user regular expressions to query our Database simillar to the behavior of the API (Search in the same fields).

### Config
All configuration is done in the [config file](config.json).

The options are:
* BASE_URL - the base url for the API
* CONNECTION_STRING - connections string to the MongoDB database
* DB_NAME - name of the database
* RESOURCES - map between the diffrent resources and the fields that are searchable.


