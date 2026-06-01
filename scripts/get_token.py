import requests, dotenv, os

dotenv.load_dotenv(".env", override=True)

N8N_URL = os.environ["N8N_URL"]


def get_token(email, password):
    response = requests.post(
        N8N_URL + "/rest/login",
        headers={"Content-Type": "application/json"},
        json={"emailOrLdapLoginId": email, "password": password},
    )

    if response.status_code == 200:
        return response.headers["Set-Cookie"].split("=")[1].split(";")[0]
    else:
        print(response.text)


print(get_token("user@user.com", "User123"))
