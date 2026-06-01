import requests, dotenv, os, secrets, json, glob

dotenv.load_dotenv(".env", override=True)

N8N_API_ADMIN_KEY = os.environ["N8N_API_ADMIN_KEY"]
N8N_URL = os.environ["N8N_URL"]

CREDENTIALS=[]
jsonPaths=glob.glob("credential_jsons/*")
for path in jsonPaths:
    with open(path,"r") as f:
        CREDENTIALS.append(json.load(f))

WORKFLOWS=[]
jsonPaths=glob.glob("workflow_jsons/*")
for path in jsonPaths:
    with open(path,"r") as f:
        WORKFLOWS.append(json.load(f))

user = {"email":"deneme33@deneme.com","firstName": "Name", "lastName": "Surname"}

def create_user(user: dict):
    print(f"\nAccount creation started for: {user['email']}")
    set_random_passwords(user)
    get_invitation_links(user)
    accept_invitations(user)
    create_api_key(user)
    import_credentials(user)
    import_workflows(user)
    delete_api_key(user)
        

def set_random_passwords(user):
    user["password"] = "Y1" + secrets.token_urlsafe(11)


def get_invitation_links(user):
    response = requests.post(
        N8N_URL + "/api/v1/users",
        headers={
            "Content-Type": "application/json",
            "X-N8N-API-KEY": N8N_API_ADMIN_KEY,
        },
        json=[{"email": user["email"], "role": "global:member"}],
    )

    if response.ok and len(response.json())==1:
        invitation=response.json()[0]

        if invitation["error"] == "":
            user["registerToken"] = invitation["user"]["inviteAcceptUrl"].split("=")[-1]
            print("Get Invitation Done!")
        else:
            print("Get Invitation Link Error -", invitation["error"]+"\n\n")
    else:
        print("Get Invitation Link Error -",response.text+"\n\n")
        raise Exception()


def accept_invitations(user):
    response = requests.post(
        N8N_URL + "/rest/invitations/accept",
        headers={
            "Content-Type": "application/json"
        },
        json={
            "firstName": user["firstName"],
            "lastName": user["lastName"],
            "password": user["password"],
            "token": user["registerToken"]
        }
    )

    if response.ok:
        user["loginToken"] = response.headers["Set-Cookie"].split("=")[1].split(";")[0]
        print("Accept Invitation Done!")
    else:
        print("Register Credentials Error","-",response.text+"\n\n")
        raise Exception()

def create_api_key(user):
    payload={
        "label": "temp",
        "expiresAt": None,
        "scopes": [
            "credential:create",
            "credential:delete",
            "workflow:create",
            "workflow:delete",
            "workflow:list",
            "workflow:read",
            "workflow:update"
        ]
    }

    response = requests.post(
        N8N_URL + "/rest/api-keys",
        headers={"Content-Type": "application/json"},
        cookies={"n8n-auth": user["loginToken"]},
        json=payload
    )

    if response.ok:
        responseBody=response.json()
        user["apiKey"]={"id":responseBody["data"]["id"], "value":responseBody["data"]["rawApiKey"]}
        print("Create API Key Done!")
    else:
        print("Create API Key Error","-",response.text+"\n\n")
        raise Exception()
    

def delete_api_key(user):
    response = requests.delete(
        N8N_URL + "/rest/api-keys/"+user["apiKey"]["id"],
        headers={"Content-Type": "application/json"},
        cookies={"n8n-auth": user["loginToken"]},
    )

    if response.ok and response.json()["data"]["success"]==True:
        print("Delete API Key Done!")
    else:
        print("Delete API Key Error","-",response.text+"\n\n")
        raise Exception()


def import_credentials(user):
    for data in CREDENTIALS:
        response = requests.post(
            N8N_URL+"/rest/credentials",
            headers={"Content-Type": "application/json"},
            cookies={"n8n-auth": user["loginToken"]},
            json=data
        )

        if response.ok:
            pass
        else:
            print("Import Credentials Error",response.text)
            raise Exception()
    print("Import Credentials Done!")

def import_workflows(user):
    for data in WORKFLOWS:
        response = requests.post(
            N8N_URL+"/rest/workflows",
            headers={"Content-Type": "application/json"},
            cookies={"n8n-auth": user["loginToken"]},
            json=data
        )

        if response.ok:
            pass
        else:
            print("Import Workflows Error",response.text)
            raise Exception()
    print("Import Workflows Done!")


create_user(user)
print(user)

