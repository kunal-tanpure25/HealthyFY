# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import wikipediaapi
from geopy.distance import great_circle
import folium
from geopy.geocoders import Nominatim

class ActionDiseaseDescription(Action):
    def name(self) -> Text:
        return "action_disease_description"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        disease_entity = next(tracker.get_latest_entity_values("disease"), None)
        if disease_entity:
            headers = {'User-Agent': 'Your_Custom_User_Agent'}  # Replace 'Your_Custom_User_Agent' with your custom user agent
            wiki_wiki = wikipediaapi.Wikipedia('en', headers=headers, extract_format=wikipediaapi.ExtractFormat.WIKI)
            page = wiki_wiki.page(disease_entity)
            if page.exists():
                summary = page.summary[:1000]  # Limit summary to 1000 characters
                dispatcher.utter_message(text=summary)
            else:
                dispatcher.utter_message(text="Sorry, I couldn't find information about that disease.")
        else:
            dispatcher.utter_message(text="Please specify a disease.")

        return []

class ActionNearestHospital(Action):
    def name(self) -> Text:
        return "action_nearest_hospital"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        geolocator = Nominatim(user_agent="rasa_bot")
        user_location = tracker.get_slot("location")
        if user_location:
            user_latitude, user_longitude = user_location.get("latitude"), user_location.get("longitude")
            if user_latitude and user_longitude:
                user_coords = (user_latitude, user_longitude)
                hospitals = [(51.509865, -0.118092), (51.508876, -0.124172), (51.507878, -0.129225)]  # Sample hospital coordinates
                nearest_hospitals = sorted(hospitals, key=lambda x: great_circle(user_coords, x).miles)[:5]
                map = folium.Map(location=user_coords, zoom_start=15)
                for hospital in nearest_hospitals:
                    folium.Marker(hospital).add_to(map)
                map.save("nearest_hospitals.html")
                dispatcher.utter_message(text="Here are the nearest hospitals:")
                dispatcher.utter_message(text="You can view them on the map: nearest_hospitals.html")
            else:
                dispatcher.utter_message(text="Please provide your current location.")
        else:
            dispatcher.utter_message(text="Please provide your current location.")

        return []
