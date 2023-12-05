import httpx
import json, os, time

with open("settings.json", "r") as regen:
    g = json.load(regen)

class Facebook_api():
    def __init__(self, pagetoken, maintoken):
        self.token_page = pagetoken
        self.token_main = maintoken
        self.reqclient = httpx.Client()


    def get_info_page(self):
        data = self.reqclient.get(f"https://graph.facebook.com/v18.0/me?access_token={self.token_page}")
        try:
            return data.json()
        except:
            raise f"Error: CANT GET INFO {data.text}"
    
    def post_page(self, data):
        pageiddata = self.get_info_page()
        idpage = pageiddata['id']
        
        datapost = self.reqclient.post(f"https://graph.facebook.com/v18.0/{idpage}/feed?message={data}&access_token={self.token_page}")
        try:
            idpost = datapost.json()
            return idpost['id']
        except:
            print(f"Error: CANT POST {datapost.text}")

    def get_all_group(self):
        data = self.reqclient.get(f"https://graph.facebook.com/v16.0/me/groups?access_token={self.token_main}")
        try:
            return data.json()
        except:
            raise f"Error: CANT GET INFO {data.text}"
    
    def post_to_grroup(self, group_id, message):

        data = self.reqclient.post(f"https://graph.facebook.com/v16.0/{group_id}/feed?access_token={self.token_main}", data={'message':message})

        try:
            idpost = data.json()
            return idpost['id']
        except:
            raise f"Error: CANT POST {data.text}"


api = Facebook_api(g['page_token'], g['main_token'])
print("ALL Token Login..")
time.sleep(0.4)
os.system("cls")
print("[1] Post Group [2] Post Page")
choise = int(input(">> "))
if choise == 1:
    allgroups = api.get_all_group()
    # Accessing the 'data' key containing the list of items
    items = allgroups.get('data', [])

    # Printing IDs and names as a list
    for idx, item in enumerate(items, start=1):
        print(f"{idx} {item['name']} - {item['id']}")
    
    group_sel = int(input("Group Number > "))

    if 1 <= group_sel <= len(items):
        selected_group = items[group_sel - 1]
        print(f"Selected Group: {selected_group['name']} - {selected_group['id']}")
    else:
        print("Invalid choice")

    Message_post = input("Message Post > ")
    
    post = api.post_to_grroup(selected_group['id'], Message_post)
    print(post)
    os.system("pause")


if choise == 2:
    data = input("Mesage Post > ")
    postpage = api.post_page(data)
    print(postpage)
    os.system("pause")
