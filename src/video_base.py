import sqlite3


class VideoBase:


    def create_video_table():
        try:
            sqliteConnection = sqlite3.connect('casino_video.db')
            sqlite_create_table_query = '''CREATE TABLE video_table (
                                        id INTEGER PRIMARY KEY,
                                        location TEXT NOT NULL,
                                        time TEXT NOT NULL,
                                        video BLOB NOT NULL);'''

            cursor = sqliteConnection.cursor()
            print("Successfully Connected to SQLite")
            cursor.execute(sqlite_create_table_query)
            sqliteConnection.commit()
            print("SQLite table created")

            cursor.close()

        except sqlite3.Error as error:
            print("Error while creating a sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("sqlite connection is closed")

    def convertToBinaryData(filename):
        # Convert digital data to binary format
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData

    def insertBLOB(id_video, loaction, time, video):
        try:
            sqliteConnection = sqlite3.connect('casino_video.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite Casino Video")
            sqlite_insert_blob_query = """ INSERT INTO video_table(id, location, time, video) VALUES (?, ?, ?, ?)"""
            video_bin = VideoBase.convertToBinaryData(video)
            # Convert data into tuple format
            data_tuple = (id_video, loaction, time, video_bin)
            cursor.execute(sqlite_insert_blob_query, data_tuple)
            sqliteConnection.commit()
            print("Video inserted successfully as a BLOB into a table")
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert blob data into sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("The sqlite connection is closed")

    def writeTofile(data, filename):
        # Convert binary data to proper format and write it on Hard Disk
        with open(filename, 'wb') as file:
            file.write(data)
        print("Stored blob data into: ", filename, "\n")

    def fiBlobData(location, time):
        try:
            sqliteConnection = sqlite3.connect('casino_video.db')
            cursor = sqliteConnection.cursor()
            print("Connected to Casino Video")

            sql_fetch_blob_query = """SELECT * from video_table where location = ? and time = ?"""
            cursor.execute(sql_fetch_blob_query, (location, time))
            record = cursor.fetchall()
            for row in record:
                print("Id = ", row[0], "Location = ", row[1], "Time= ", row[2])
                video_locaction = row[1]
                video_time = row[2]
                video = row[3]

                print("Storing video on disk \n")
                videoPath = "E:\Pobrane\\" + video_locaction + ".mp4"
                VideoBase.writeTofile(video, videoPath)
                
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to read blob data from sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("The Sqlite connection is closed")

    def viewBlobData():
        try:
            sqliteConnection = sqlite3.connect('casino_video.db')
            cursor = sqliteConnection.cursor()
            print("Connected to Casino Video")

            sql_fetch_blob_query = """SELECT id, location, time from video_table"""
            cursor.execute(sql_fetch_blob_query)
            record = cursor.fetchall()
            for row in record:
                print("Id = ", row[0], "Location = ", row[1], "Time= ", row[2])       
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to read blob data from sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("The Sqlite connection is closed")


VideoBase.create_video_table()
VideoBase.insertBLOB(1, "lobby", "2023-04-13 13:57:01", "E:\Pobrane\mrowka.mp4")
#VideoBase.insertBLOB(2, "foyer", "2023-04-13 14:37:01", "E:\Pobrane\mrowka2.mp4")
#VideoBase.insertBLOB(3, "atrium", "2023-04-12 12:37:01", "E:\Pobrane\mrowka3.mp4")


VideoBase.readBlobData("lobby", "2023-04-13 13:57:01")
#VideoBase.readBlobData("foyer", "2023-04-13 14:37:01")
#VideoBase.readBlobData("atrium")
VideoBase.viewBlobData()
