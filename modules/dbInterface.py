import sqlite3
from pathlib import Path

def loadImagelistFromDB():
    try:
        sqliteConnection = sqlite3.connect('data.sqlite')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        
        sqlite_filenames_selection_query = """ SELECT filename FROM images """

        cursor.execute(sqlite_filenames_selection_query)
        rows = cursor.fetchall()        
        cursor.close()
        
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed") 
            
    return [r[0] for r in rows]
    
def loadImageFromDB(imageFileName):
    try:
        sqliteConnection = sqlite3.connect('data.sqlite')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        
        sqlite_imagedata_selection_query = """ SELECT imagedata FROM images WHERE filename=(?)"""

        cursor.execute(sqlite_imagedata_selection_query,(imageFileName))
        imageData = cursor.fetchone()        
        cursor.close()
        
    except sqlite3.Error as error:
        print("Failed to read image data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed") 
    return imageData

def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData   

def saveImageToDB(imageFilePath):
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


def deleteImageFromDB(imageFileName):
    try:
        sqliteConnection = sqlite3.connect('data.sqlite')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        
        sqlite_imagedata_delete_query = """ DELETE FROM images WHERE filename=:filename;"""

        cursor.execute(sqlite_imagedata_delete_query,{"filename":imageFileName})
        sqliteConnection.commit()
        cursor.close()
        print(f"Deleting {imageFileName}")
    except sqlite3.Error as error:
        print("Failed to delete image data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed") 
            

def getImageId(cursor, imageFileName):
     cursor.execute(""" SELECT id FROM images WHERE filename=:filename""",{"filename":imageFileName})
     imageID = cursor.fetchone()  
     return imageID[0]
            
            
def addImageNoteToDB(imageName, imageNote):
    try:
        sqliteConnection = sqlite3.connect('data.sqlite')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        
        imageID = getImageId(cursor, imageName[0])
        print(f"From image {imageName[0]} got image ID {imageID}")
        sqlite_insert_image_note_query = """ INSERT INTO imagenotes
                                  (note,image_ref) VALUES (?, ?)"""
        cursor.execute(sqlite_insert_image_note_query, (imageNote,imageID))
        sqliteConnection.commit()
        cursor.close()
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")
               
            
            
            
            
            
            
            
            
            
