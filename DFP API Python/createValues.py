from googleads import dfp
import os

path = os.path.dirname(__file__)
credential_path = "%s/Credentials/googleads.yaml" % (os.path.abspath(path))

def main():

    key_id = str(input('''

    You will need to go create the hb_pb key in DFP, if you haven't already. When you create it, the key ID should be
    in the URL.

    Past it here ->>>>>>>>>>>>'''))

    numberOfValues = int(input('''

    How Many 1c values would you like created in your hb_pb key? I'd suggest 15,000 (so up to $150 in 1c increments)
    Paste your number here ->>>>>

    '''))

    custom_targeting_service = dfp_client.GetService('CustomTargetingService', version='v201611' )
    for x in range(1,numberOfValues + 1):
        try:
            values = []
            values.append({
                'customTargetingKeyId': key_id,
                'displayName': '{0:.2f}'.format(x / 100),
                'name': '{0:.2f}'.format(x / 100),
                'matchType': 'EXACT'
            })
            values = custom_targeting_service.createCustomTargetingValues(values)
        except Exception:
            print("Value already created. Moving on to next one.")
            pass
    print("Script Complete")


dfp_client = dfp.DfpClient.LoadFromStorage(path=credential_path)
main()