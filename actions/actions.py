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


import psycopg2

class ActionUserName(Action):

    def name(self) -> Text:
        return "action_user_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        conn = None
        try:
            print("-----------")
            print(tracker.get_latest_input_channel())
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
            if tracker.get_latest_input_channel()=="twilio":
                dispatcher.utter_message(text="Please write user name")
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
            if tracker.get_latest_input_channel()=="twilio":
                dispatcher.utter_message(text="Please write user name")
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

        return [SlotSet('orderid',None)]

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

        return [SlotSet('materialid',None)]

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
        return []

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

        return [SlotSet('orderid',None)]


# class ActionResourcesList(Action):

#     def name(self) -> Text:
#         return "action_test"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         data= [ { "title": "Sick Leave", "description": "Sick leave is time off from work that workers can use to stay home to address their health and safety needs without losing pay." }, { "title": "Earned Leave", "description": "Earned Leaves are the leaves which are earned in the previous year and enjoyed in the preceding years. " }, { "title": "Casual Leave", "description": "Casual Leave are granted for certain unforeseen situation or were you are require to go for one or two days leaves to attend to personal matters and not for vacation." }, { "title": "Flexi Leave", "description": "Flexi leave is an optional leave which one can apply directly in system at lease a week before." } ]

#         message={ "payload": "collapsible", "data": data }

#         dispatcher.utter_message(text="You can apply for below leaves",json_message=message)
#         dispatcher.utter_message(text="-----------")
#         # dispatcher.utter_message(attachment=message)
#         return []

class ActionCarousel(Action):
    def name(self) -> Text:
        return "action_carousel"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        data = {
        "payload": 'cardsCarousel',
        "data": [
            {
                "image": "https://b.zmtcdn.com/data/pictures/1/18602861/bd2825ec26c21ebdc945edb7df3b0d99.jpg",
                "title": "Taftoon Bar & Kitchen",
                "ratings": "4.5",
            },
            {
                "image": "https://b.zmtcdn.com/data/pictures/4/18357374/661d0edd484343c669da600a272e2256.jpg",

                "ratings": "4.0",
                "title": "Veranda"
            },
            {
                "image": "https://b.zmtcdn.com/data/pictures/4/18902194/e92e2a3d4b5c6e25fd4211d06b9a909e.jpg",

                "ratings": "4.0",
                "title": "145 The Mill"
            },
            {
                "image": "https://b.zmtcdn.com/data/pictures/3/17871363/c53db6ba261c3e2d4db1afc47ec3eeb0.jpg",

                "ratings": "4.0",
                "title": "The Fatty Bao"
            },
        ]
    }

        dispatcher.utter_message(json_message=data)
        return []

class ActionCollapsible(Action):
    def name(self) -> Text:
        return "action_collapsible"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        data= [ { "title": "Sick Leave", "description": "Sick leave is time off from work that workers can use to stay home to address their health and safety needs without losing pay." }, { "title": "Earned Leave", "description": "Earned Leaves are the leaves which are earned in the previous year and enjoyed in the preceding years. " }, { "title": "Casual Leave", "description": "Casual Leave are granted for certain unforeseen situation or were you are require to go for one or two days leaves to attend to personal matters and not for vacation." }, { "title": "Flexi Leave", "description": "Flexi leave is an optional leave which one can apply directly in system at lease a week before." } ]

        message={ "payload": "collapsible", "data": data }

        dispatcher.utter_message(text="You can apply for below leaves",json_message=message)
        return []
