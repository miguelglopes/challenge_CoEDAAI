# CoE DAAI Python Test

*Author: Miguel Gomes Lopes*

This folder contains my solutions for the CoE DAAI Python Test

It is divided between 2 sub-folders: Part1 and Part2. It also contains my configurations for VSCode, which was the editor I used for the project. You can find 2 debug configurations (launch.json in the .vscode folder), one for Part1 and another for Part2, as well as the settings.json.

I used a python virtual environment to better contain the project, which can be found in the folder pythonTestVenv.

All the code respects the Python Enhancement Proposal (PEP8).

## PART1

This folder contains the following structure:


    ├──.vscode                      # Visual Studio Code settings
    ├── Part1                       # Part1
        ├── data                
            ├── config.py           # Configuration file
            ├── preciosEESS_es.xls  # Provided data
        ├── project             
            ├── DataExcel.py        # Answers to P1E1
            ├── SQLModel.py         # Answers to P1E2
            ├── SQLController.py    # Answers to P1E2
            ├── main.py             # script with the full pipeline
        ├── dashboard.pbix          # powerBI file
    ├── Part2                       # Part2
    ├── pythonTestVenv              # Virtual Environment

My goal with this part of the project was to develop a small program that would allow the excel data to be read, processed and automatically inserted to an SQL database. I also wanted the historical data to be available, i.e., if a new file, from a different time of the day is processed, I wanted to keep the old data.
Analysing the data, I concluded that the best way to store this data would be with the following SQL tables structure, which guarantees data integrity, consistency and avoids redundancy:
![alt text](Part1\tables.png)

As can be seen, a station is described by its location (longitude, latitude, direccion, codigo postal, margen, localidade, municipio, provincia). After carefully analyzing the data, I found that an appropriate unique constraint would be (Longitude, Latitude, Margen). The table  contains the actual product price data. Each  is defined by a Station, a product, its price at a given time (fecha), as well as the brands, venta etc.

Although this structure is very good in terms of integrity, consistency, redundancy and relationship, it becomes cumbersome to insert data manually, due to all the integrity constraints. Therefore I decided to use an ORM (Object-relational mapping), in this case, SQLAlchemy, to interact with the database. Although this may complexify this specific exercise, in the long term it becomes much more manageable, and, since we have a Data Model, allows to easily change the data storage engine without changing the code. Furthermore, since I had to do this project, I used it as an opportunity to learn ORM in Python, since I only had use ORM's in Java and C#.

The Model part of the ORM, that defines the classes that represent each table and the relationships between them, is coded in the SQLModel.py. The controller part, that bridges the excel data to the sql data and allows the insertion of all data, is in the SQLController.py file. In order to store the data of the excel file, including its date of creation, I decided to create a class ExcelFile. This way, multiple files can be easily inserted with 1 line of code. The file main.py has an example of the steps needed to get the data from the excel file and store it in the MySQL database. This was the file I run to populate the database stations that is then used to connect to powerBI (dashboard.pbix). Regarding the dashboard in powerBI, I don't really enjoy doing data visualization and I'm not very proud of the final result.

I've included some comments in the code, as well as docstrings.

## Part2

This folder has the following structure:

    ├──.vscode                      # Visual Studio Code settings
    ├── Part1                       # Part1
    ├── Part2                       # Part2
        ├── data                
            ├── config.py           # Configuration file
            ├── countries.json      # Provided countries .json
        ├── project             
            ├── test.py             # Answers to the 8 questions
        ├── test
            ├── test.py             # Unit tests
    ├── pythonTestVenv              # Virtual Environment

The data folder contains the configuration file as well as the provided countries JSON file. For simplicity, the configuration file is a python file with a dictionary of immutable data. It could also be done in JSON or YAML.

The test.py file is in the project folder, and answers to the 8 questions of Part 2. I've included some comments in the code, as well as docstrings.

In order to test the methods and classes created, I've included 8 unit tests in the tes_test.py file that can easily be run to validate the results.