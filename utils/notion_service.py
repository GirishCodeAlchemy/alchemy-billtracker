import json

import requests


class NotionDatabaseHandler:
    def __init__(self, api_key, database_id, category_db_id, mode_db_id):
        self.api_key = api_key
        self.database_id = database_id
        self.category_db_id = category_db_id
        self.mode_db_id = mode_db_id
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",  # Latest API version
        }

    def get_database_schema(self):
        url = f"https://api.notion.com/v1/databases/{self.database_id}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            print("Schema fetched successfully.")
            return response.json()
        else:
            print(f"Failed to fetch schema: {response.status_code} - {response.text}")
            return None

    def search_database(self, database_id, query):
        url = f"https://api.notion.com/v1/databases/{database_id}/query"
        search_payload = {
            "filter": {
                "property": "Name",  # Assumes the property to search by is 'Name'
                "title": {"contains": query},
            }
        }
        response = requests.post(
            url, headers=self.headers, data=json.dumps(search_payload)
        )

        if response.status_code == 200:
            results = response.json()
            if results["results"]:
                return results["results"][0]["id"]  # Return the first matching page ID
            else:
                print(
                    f"No matching pages found for '{query}' in database '{database_id}'."
                )
                return None
        else:
            print(
                f"Failed to search database: {response.status_code} - {response.text}"
            )
            return None

    def create_entry_payload(self, user_content):
        schema = self.get_database_schema()
        if not schema:
            return None

        properties = schema["properties"]
        entry_payload = {"parent": {"database_id": self.database_id}, "properties": {}}

        for key, value in user_content.items():
            if key in properties:
                prop_type = properties[key]["type"]
                if prop_type == "title":
                    entry_payload["properties"][key] = {
                        "title": [{"type": "text", "text": {"content": value}}]
                    }
                elif prop_type == "rich_text":
                    entry_payload["properties"][key] = {
                        "rich_text": [{"type": "text", "text": {"content": value}}]
                    }
                elif prop_type == "number":
                    entry_payload["properties"][key] = {"number": value}
                elif prop_type == "date":
                    entry_payload["properties"][key] = {"date": {"start": value}}
                elif prop_type == "files":
                    entry_payload["properties"][key] = {
                        "files": [
                            {
                                "name": value["name"],
                                "type": "external",
                                "external": {"url": value["url"]},
                            }
                        ]
                    }
                elif prop_type == "relation":
                    # Dynamically find the related page IDs
                    if key == "Category":
                        related_page_id = self.search_database(
                            self.category_db_id, value
                        )
                    elif key == "Mode":
                        related_page_id = self.search_database(self.mode_db_id, value)
                    else:
                        related_page_id = None

                    if related_page_id:
                        entry_payload["properties"][key] = {
                            "relation": [{"id": related_page_id}]
                        }
                    else:
                        print(
                            f"Related page ID not found for {key} with value '{value}'"
                        )
                elif prop_type == "select":
                    entry_payload["properties"][key] = {"select": {"name": value}}
                elif prop_type == "multi_select":
                    entry_payload["properties"][key] = {
                        "multi_select": [{"name": v} for v in value]
                    }

                # Add other property types as needed

        return entry_payload

    def insert_entry(self, entry_payload):
        url = "https://api.notion.com/v1/pages"
        response = requests.post(
            url, headers=self.headers, data=json.dumps(entry_payload)
        )

        if response.status_code == 200:
            print("Entry inserted successfully.")
            return response.json()
        else:
            print(f"Failed to insert entry: {response.status_code} - {response.text}")
            return None
