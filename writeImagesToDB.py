import sqlite3
import glob
from pathlib import Path

def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insertImage(imageFilePath):
    try:
        sqliteConnection = sqlite3.connect('data.sqlite')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = """ INSERT INTO images
                                  (imagedata, filename, extension) VALUES (?, ?, ?)"""

        image = convertToBinaryData(imageFilePath)

        path = Path(imageFilePath) 
        filename = str(path.stem)
        fileExtension = str(path.suffixes)
        data_tuple = (image, filename, fileExtension)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")

for imageFile in glob.glob('*'):
    print(f'Inserting {imageFile}')
    insertImage(imageFile)
