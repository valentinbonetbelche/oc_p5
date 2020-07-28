# OC_P5

OC_P5 is a Python-based app that will let you select a food reference from the OpenFoodFact Database through their API and will display you healthier options.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.

```bash
pip install -r requirements.txt
```

You will need a Mysql server up and running with a database named ```oc_p5```.

You can edit the name of the database by modifying the ```database_name``` variable inside the ```main.py``` file, line 8.

## Usage

You can launch the program through your regular IDE or by executing the following command in your terminal
```bash
python3 main.py
```
or
```bash
python main.py
```

## Functionnalities

#### Login

The user can login with his *username* and *password*.

#### Register

The user can register and choose his *username* and *password*.

#### Replace My Product!

The app displays to the user the list, as a table, of all the products for a specified category.
The user can then select a product from the list by its Id and the app will display him a second list, of healthier options.
He can then select a healthier product and can choose to save his replacement, if he's logged in.

#### My Saved Products

The app displays the list of all the user's saved products, if he's logged in.

#### Categories list

The app displays the list of the categories, saved in the database.

#### Products Importer

The user can import the products from the Open Food Facts API, for a selected category.