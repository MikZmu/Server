import sqlite3
import datetime
import os
import random

class VideoBase:
    def isLinux():
        print("IsLinux")
        from sys import platform
        global linuxMode
        if(platform == "linux" or platform == 'linux2'):    
            return 1
        else:
            return 0

    def create_video_table():
        try:
            sqliteConnection = sqlite3.connect('casino_video.db')
            sqlite_create_table_query = '''CREATE TABLE video_table (
                                        id INTEGER PRIMARY KEY,
                                        location TEXT NOT NULL,
                                        time DATETIME  NOT NULL,
                                        video TEXT NOT NULL);'''

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

    def dataToTable(location, startTime, endTime):
        try:
            if(location=='ANY'):
                sql_fetch_blob_query = """SELECT * 
                from video_table where
                AND time >= ? 
                AND time <= ?"""
            sqliteConnection = sqlite3.connect('casino_video.db')
            cursor = sqliteConnection.cursor()
            tuple = (location,startTime, endTime,)
            sql_fetch_blob_query = """SELECT * 
            from video_table where
            location = ? 
            AND time >= ? 
            AND time <= ?"""
            cursor.execute(sql_fetch_blob_query, tuple)
            record = cursor.fetchall()   
            cursor.close()
            return record
        except Exception as e:
            print(e)

    def insertVid(id_video, loaction, time, video):
        try:
            sqliteConnection = sqlite3.connect('casino_video.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite Casino Video")
            sqlite_insert_blob_query = """ INSERT INTO video_table(id, location, time, video) VALUES (?, ?, ?, ?)"""
            # Convert data into tuple format
            data_tuple = (id_video, loaction, time, video)
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
                

    def playQuery(id):
        try:
            sqliteConnection = sqlite3.connect('casino_video.db')
            cursor = sqliteConnection.cursor()
            tuple = (id,)
            sql_fetch_blob_query = """SELECT * 
            from video_table where
            id = ?"""
            cursor.execute(sql_fetch_blob_query, tuple)
            record = cursor.fetchall()   
            cursor.close()
            return record
        except Exception as e:
            print(e)

    def baseInit2():
        initFlag = 0
        try:
            os.remove("casino_video.db")
        except:
            print('nothing')
        try:
            VideoBase.create_video_table()
        except:
            print('nothing')
        if(VideoBase.isLinux() == 1):
            names = os.listdir(path='vids/')
            app = ""
        else:
            names = os.listdir(path='src/vids/')
            app = 'src/'
        for path in names:
            print(path)
            if(path.lower().endswith(".mp4")):
                try:
                    pthSpl = path.split('/')
                    name = pthSpl[len(pthSpl)-1]
                    print(name)
                    nameSpl = name.split('&')
                    date = nameSpl[1].split(' ')
                    date1 = date[0]
                    date2 = date[1].replace('-',':')
                    VideoBase.insertVid(str(hash(path))[0:4],nameSpl[0],date1 + ' ' + date2.replace('.mp4', ""), app + 'vids/' + path)
                except:
                    initFlag = 1
        return initFlag

            

    """def baseInit():
        VideoBase.create_video_table()
        VideoBase.insertVid(1, "lobby", "2011-04-13 00:45:01", "src/vids/bear_sits.mp4")
        VideoBase.insertVid(2, "atrium", "2016-02-13 01:40:01", "/src/vids/black_father_rare_footage.mp4")
        VideoBase.insertVid(3, "foyer", "2013-06-13 05:20:01", "/vids/desk.mp4")
        VideoBase.insertVid(4, "lobby", "2017-08-13 06:00:01", "vids/dog_swing.mp4")
        VideoBase.insertVid(5, "atrium", "2015-05-13 13:57:01", "src/vids/doge.mp4")
        VideoBase.insertVid(6, "foyer", "2019-03-13 10:25:01", "src/vids/eyes.mp4")
        VideoBase.insertVid(7, "lobby", "2016-01-13 11:00:01", "src/vids/feet_on_sand.mp4")
        VideoBase.insertVid(8, "atrium", "2012-07-13 12:05:01", "src/vids/hands_laptop.mp4")
        VideoBase.insertVid(9, "foyer", "2023-09-13 12:50:01", "src/vids/hors.mp4")
        VideoBase.insertVid(10, "lobby", "2022-10-13 16:50:01", "src/vids/lions.mp4")
        VideoBase.insertVid(11, "atrium", "2020-11-13 21:15:01", "src/vids/sanitizer.mp4")
        VideoBase.insertVid(12, "foyer", "2021-12-13 23:10:01", "src/vids/tired.mp4")"""
