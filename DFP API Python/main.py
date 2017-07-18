import os
from creatives import creative
from getLineItemID import getLineItems
from createLineItem import createLineItem
from getTargetingValues import getTargetingValues
print("\n\n\nI would HIGHLY recommend creating a testing order to run this script on before using it on a main one.\n\n\n")

order_id = str(input("Please enter your Order ID here: ->>>> "))

print('''

The next part requires that you create a placement in DFP. This is a collection of all the ad units you
want to use for Prebid. Go do that now if you haven't already and enter the ID below

''')

adunit_id = input('''

Please enter the Ad Unit Id you want to associate with each line item. These can be found here:
    dfp ->> inventory tab ->>> ad units - >>> search for your ad unit ->> URL

    https://www.google.com/dfp/1234#inventory/inventory/adSlotId=123456

Please paste them in the following format:
1234567890,23456788,1234567890

''').split(',')
adunit_id = list(map(int, adunit_id))
creative_ids = input('''


Next Step is to enter your creative IDs. Until this point, we've created a bunch of line items but haven't yet attached the necessary prebid creatives to them.

You will need one creative for each ad unit you want to use. Ideally you already have these created.

Please enter all the IDs you wish to use in the following format:

1234567890,23456788,1234567890
->>>> ''').split(',')
creative_id = list(map(int, creative_ids))


key_id = str(input('''

Next thing you will need is your KEY VALUE ID. For example, Prebid uses hb_pb as the key value.
You can find this ID value by going to:

    DFP ->>> Inventory ->>> Key-Values ->>> Search for your Prebid hb_pb key ->>> Click on it.
    The Key Value ID should be in the URL. If you haven't created that yet, go create it and check out
    the createValues script in this directory.


Past it here ->>>>>>>>>>>>'''))
increment = float(input('''
Now we need the increment which the line items increase by. Please enter this value in decimal format. For example:

    1c increment = 0.01
    10c increment = 0.1
    50c increment = 0.5
    $1 increment - 1.0

->>>>>>>>'''))
startingAmount = float(input('''

Please also enter the starting amount in decimal format. This will be the rate of the FIRST line item you wanted created.
So if you want line items created between $1 and $5, this value would be 1.00. Also remember that you have
already had to create one line item when you created your prebid order. If that default line item is 1.00, and you
want it to increment 10c every time, then this value should be 1.10.


->>>>>'''))
numberOfLines = int(input('''

    Finally we need the number of line items you want created. You will need to work out how many lines items it takes
    between your desired amounts.

'''))
print("Script Commencing...")

def main():
    path = os.path.dirname(__file__)
    credential_path = "%s/Credentials/googleads.yaml" % (os.path.abspath(path))


    getValues = getTargetingValues.getValueID(key_id=key_id, path=credential_path).main()
    createLineItems = createLineItem.createLineItem(key_id=key_id, path=credential_path, order_id=order_id, adunit_id=adunit_id,increment=increment,startingAmount=startingAmount,numberOfLines=numberOfLines).main(targetingValues=getValues)
    print("Now getting all line Item IDs and assigning your prebid creatives to them")
    getLineItem = getLineItems.getLineItemID(path=credential_path, order_id=order_id).main()
    for line_item in getLineItem:
        for creativeID in creative_id:
            try:
                creatives = creative.creative(path=credential_path, creative_ids=creativeID, line_item_id=line_item, order_id=order_id).main()
            except Exception:
                print("Creative already in line item, trying next one.")
                pass
main()