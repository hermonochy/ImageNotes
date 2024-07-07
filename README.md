# ImageNotes

Program to demonstrate using sqlite in Python for storing large binary data, such as images. 

Script `writeImagesToDB.py` reads files from current directory and writes data of files into a database table, together with filename and extension. 

`Viewer` shows a list of files stored in a GUI, displays these and permits deleting entries.

Only Python standard library required - No dependencies.

## Future work
- Database and tables need to be created with a separate tool. Write Python script for database and table setup.
