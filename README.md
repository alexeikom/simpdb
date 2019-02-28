DESCRIPTION:
===========
Simple file-based (CSV) DB manager written in python.
All changes are immediate! When you remove a record - it is removed directly from the db file! In future releases I will make it more sophisticated!
Currently under an active development!

CONFIG:
======
bases_dir - path to folder that will hold your databases


USAGE:
=====
1. start the main file. You will se a following menu:

	  '>c'   create db
    
    '>a'   append record to db
    
    '>p'   print db
    
    '>r'   remove record
    
    '>sa'  set active db
    
    '>q'   quit
	
An active db can be specified by >sa command (or indirectly, after >c, >p or >r command). After the active database has been chosen, all subsequent commands will be applied to this db.

	>c - create a new file for db (after that active db will be the one you created). You will have a prompt for each column name. When done, just hit enter on the next prompt.
	>a - append a new record to db. There will be a prompt for each column name or you can specifiy the whole record with coммаs as dividers. E.g., dog,2,jack for a database with columns 'animal',
	'age' and 'name'
	>p - prints the active db with an addition of enumeration column. This is for reference to records by numbers. Uses prettytable package for that.
	>r - remove a record. All record manipulations are done by record numbers (see >p command). So, for example, to remove records 2,3 and 5-10 I will specify after >r prompt 2,3,5-10.
	>sa - set an active db (the one you want to work on now).
	>q - quit
	
EXAMPLE:
=======
	
	>c
	animals
	animal
	age
	name
	>p
	
output:

+-------+--------+-----+------+

| ser # | animal | age | name |

+-------+--------+-----+------+

+-------+--------+-----+------+

	>a
	dog,2,spike
	>a
	cat,5,twinkie
	>p

output:

+-------+--------+-----+---------+

| ser # | animal | age |   name  |

+-------+--------+-----+---------+

|   0   |  dog   |  2  |  spike  |

|   1   |  cat   |  5  | twinkie |

+-------+--------+-----+---------+

	>r
	1
	>p

output:

+-------+--------+-----+-------+

| ser # | animal | age |  name |

+-------+--------+-----+-------+

|   0   |  dog   |  2  | spike |

+-------+--------+-----+-------+
