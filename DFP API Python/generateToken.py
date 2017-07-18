from oauth2client import client

def getTokens():

    print("If you haven't read the README and got some credentials, cancel this script and go do that.")

    need_credentials = input("Would you like to stop the script to get credentials? Type YES to do so.")
    if need_credentials.find("YES" or "yes") != -1:
        quit()


    clientID = input("Paste your client ID here: ")
    clientSecret = input("Paste your Client Secret Here: ")
    redirect_uri = input("Paste your redirect_uri here: ")
    SCOPE = u'https://www.googleapis.com/auth/dfp'


    flow = client.OAuth2WebServerFlow(
        client_id=clientID,
        client_secret=clientSecret,
        scope=SCOPE,
        user_agent='Ads Python Client Library',
        redirect_uri=redirect_uri,
        approval_prompt='force',
        access_type='offline'
    )

    authorize_url = flow.step1_get_authorize_url()
    print('Click on the following URL and login with your google account: \n%s\n' % (authorize_url))
    print ('After approving the token enter the verification code (if specified).')

    code = input('Code: ').strip()
    credential = flow.step2_exchange(code)

    print("Refresh Token for YAML: ",credential.refresh_token)
    print("Client ID: ", clientID)
    print("Client Secret: ", clientSecret)

    print("Put the ID, Secret, and Refresh Token in the YAML file. Don't run this script again")

getTokens()