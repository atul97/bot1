# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset, SlotSet
#
#
import requests

import json


# from configparser import ConfigParser
  
  
# def config(filename='database.ini', section='postgresql'):
#     # create a parser
#     parser = ConfigParser()
#     # read config file
#     parser.read(filename)
  
#     # get section, default to postgresql
#     db = {}
#     if parser.has_section(section):
#         params = parser.items(section)
#         for param in params:
#             db[param[0]] = param[1]
#     else:
#         raise Exception('Section {0} not found in the {1} file'.format(section, filename))
  
#     return db

# import psycopg2
# from config import config
  
# def connect():
#     """ Connect to the PostgreSQL database server """
#     conn = None
#     try:
#         # read connection parameters
#         params = config()
  
#         # connect to the PostgreSQL server
#         print('Connecting to the PostgreSQL database...')
#         conn = psycopg2.connect(**params)
          
#         # create a cursor
#         cur = conn.cursor()
          
#     # execute a statement
#         print('PostgreSQL database version:')
#         cur.execute('SELECT version()')
  
#         # display the PostgreSQL database server version
#         db_version = cur.fetchone()
#         print(db_version)
         
#     # close the communication with the PostgreSQL
#         cur.close()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()
#             print('Database connection closed.')


import psycopg2
# conn = psycopg2.connect(database ="gfgdb", user = "gfguser",
#                         password = "passgeeks", host = "52.33.0.1", 
#                         port = "5432")
  
class ActionUserName(Action):

    def name(self) -> Text:
        return "action_user_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        conn = None
        try:
            print("-----------")
            # uname = tracker.get_slot("uname")
            conn = psycopg2.connect(database ="rasa", user = "postgres",
                        password = "123456", host = "localhost", 
                        port = "5432")
            print("Connection Successful to PostgreSQL")

            cur = conn.cursor()
            
            query = f"""select distinct(customer_name) from visits;"""
            cur.execute(query)
            rows = cur.fetchall()
            
            buttons = []
            

            for x in rows:
                print(x[0])
                buttons.append({"title": x[0] , "payload": x[0]})

            
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
        if len(rows)==0:
            dispatcher.utter_message(text=f"No user found")
        else:
            dispatcher.utter_message(text="Please select user",buttons=buttons)

        return []

class ActionBreakdownVisit(Action):

    def name(self) -> Text:
        return "action_breakdown_visit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        conn = None
        try:
            print("-----------")
            uname = tracker.get_slot("uname")
            conn = psycopg2.connect(database ="rasa", user = "postgres",
                        password = "123456", host = "localhost", 
                        port = "5432")
            print("Connection Successful to PostgreSQL")

            cur = conn.cursor()
            
            query = f"""select * from visits where customer_name = '{uname}';"""
            cur.execute(query)
            rows = cur.fetchall()
            
            buttons = []
            

            for x in rows:
                print(x[1], x[2])
                buttons.append({"title": f'{x[1]} {x[2]}' , "payload": x[3]})

            
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
        if len(rows)==0:
            dispatcher.utter_message(text=f"No details found for user: {uname} ")
        else:
            dispatcher.utter_message(text="Here are your appointment details:",buttons=buttons)

        return []

class ActionOrder(Action):

    def name(self) -> Text:
        return "action_orderid"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        conn = None
        text = ""

        print("*************")
        try:
            print("-----------")
            orderid = tracker.get_slot("orderid")

            conn = psycopg2.connect(database ="rasa", user = "postgres",
                        password = "123456", host = "localhost", 
                        port = "5432")
            print("Connection Successful to PostgreSQL")

            cur = conn.cursor()
            print("Before Query")
            query = f"""select * from order_details where order_id = '{orderid}';"""
            cur.execute(query)
            rows = cur.fetchall()
            
            # buttons = []
            print(rows)
            for x in rows:
                # text = ""
                text  = f"{x[1]} {x[2]} {x[3]} "

            
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
        dispatcher.utter_message(text=text)

        return []

class ActionMaterialDetails(Action):

    def name(self) -> Text:
        return "action_material_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        conn = None
        try:
            print("-----------")
            uname = tracker.get_slot("uname")
            conn = psycopg2.connect(database ="rasa", user = "postgres",
                        password = "123456", host = "localhost", 
                        port = "5432")
            print("Connection Successful to PostgreSQL")

            cur = conn.cursor()
            
            query = """select * from material_details"""
            cur.execute(query)
            rows = cur.fetchall()
            
            buttons = []
            for x in rows:
                print(x[1], x[2])
                buttons.append({"title": x[0] , "payload": x[0]})

            
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
        dispatcher.utter_message(text="I can certainly get that information for you. Could you please provide me the material numbers?",buttons=buttons)
        return [AllSlotsReset(),SlotSet('uname',uname)]

class ActionMaterialAvailability(Action):

    def name(self) -> Text:
        return "action_material_availability"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        conn = None
        text = ""
        try:
            print("-----------")
            materialid = tracker.get_slot("materialid")

            conn = psycopg2.connect(database ="rasa", user = "postgres",
                        password = "123456", host = "localhost", 
                        port = "5432")
            print("Connection Successful to PostgreSQL")

            cur = conn.cursor()
            
            query = f"""select * from material_details where materialid = '{materialid}';"""
            cur.execute(query)
            rows = cur.fetchall()
            
            # buttons = []
            for x in rows:
                # text = ""
                text  = f"Material Number :{x[0]} ,Material Description :{x[1]},Warehouse/Plant Details:{x[2]},Available Qty at Warehouse:{x[3]},Available Qty in your stock;{x[4]}"
            
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
        dispatcher.utter_message(text=text)

        return []

class ActionAllOrderStatus(Action):

    def name(self) -> Text:
        return "action_all_order_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        conn = None
        try:
            print("-----------")
            uname = tracker.get_slot("uname")
            conn = psycopg2.connect(database ="rasa", user = "postgres",
                        password = "123456", host = "localhost", 
                        port = "5432")
            print("Connection Successful to PostgreSQL")

            cur = conn.cursor()
            
            query = """select * from order_status"""
            cur.execute(query)
            rows = cur.fetchall()
            
            buttons = []
            for x in rows:
                print(x[1], x[2])
                buttons.append({"title": x[0] , "payload": x[0]})

            
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
        dispatcher.utter_message(text="Sure! I can help you with that. Could you provide the material number for the article you want to track?",buttons=buttons)
        return [AllSlotsReset()]

class ActionOrderStatus(Action):

    def name(self) -> Text:
        return "action_order_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        conn = None
        text = ""
        try:
            print("-----------")
            orderid = tracker.get_slot("orderid")

            conn = psycopg2.connect(database ="rasa", user = "postgres",
                        password = "123456", host = "localhost", 
                        port = "5432")
            print("Connection Successful to PostgreSQL")

            cur = conn.cursor()
            
            query = f"""select * from order_status where order_number = '{orderid}';"""
            cur.execute(query)
            rows = cur.fetchall()
            
            # buttons = []
            for x in rows:
                # text = ""
                text  = f"Your order for article {x[0]} is {x[2]} Here is the Reference ID:{x[1]}"
            
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
        dispatcher.utter_message(text=text)

        return []
