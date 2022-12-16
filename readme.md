# StoreProject

The program is tested on Python 3.9 

To start the program get your current working directory in the root folder, 
storeproj and write in the commandline python main.py PriceBasket and list your products.

For example
> python main.py PriceBasket Apples Milk 

To run tests first install requirements-test.txt with the following command 
> pip install -r requirements-test.txt 

Then run 
> python -m pytest

------

#### Description of the program
The program has several components:
1) main.py, current entrypoint of the program, receives the command line arguments
and passes it to runner.py 
2) runner.py, just the runner class which calls the policy from policies.py, according to the received argument,
and runs it, passing the remaining arguments. 
3) policies.py, includes the objects and functionalities 
for running different commands requested by the user (currently only PriceBasket)
with some helper functions and classes.
4) store_model.py, which includes objects and functionalities 
that describe the products and the offers, as well as the basket. 
5) db_ops.py, includes functionalities for handling the data, 
as in retrieving data.
6) calculators.py, enables running relevant calculations with the store_model objects,
as requested by a policy in policies.py.
7) format_number_representation.py, formats the numbers according to a rule,
currently pound formatter is the only one included. 

