#Guide to DFP Line Item Creations

##Setup Work

You will need python on your computer to execute this script. Head over to https://www.python.org/downloads/
and download Python 3.6.

After installing it on your machine, you should be able to execute scripts from the terminal simply by typing
'python script.name', when in the file's directory.

###Step 1 - Getting Credentials

We first need to collect security credentials. Navigate to:
    https://developers.google.com/doubleclick-publishers/docs/authentication#webapp

The script will be using the Web Application authentication type. On the page, on step 2 make sure to
select 'Web Application', as shown below.



<img width="894" alt="dfpcredentialstep1" src="https://cloud.githubusercontent.com/assets/17837150/22405589/f78a8e9a-e5f9-11e6-8ff1-826a5af9ac43.png">




Click on 'Open the Google Developers Console Credentials Page' and select 'Create a project'

<img width="417" alt="dfpcredentialstep2" src="https://cloud.githubusercontent.com/assets/17837150/22405586/f7801fdc-e5f9-11e6-87aa-aeb82072e766.png">

Name your project whatever you like. When that is created, click on 'Create Credentials' and select OAuth client ID.

<img width="428" alt="dfpcredentialstep3" src="https://cloud.githubusercontent.com/assets/17837150/22405588/f7808fbc-e5f9-11e6-8c11-5595f19b175f.png">

The application type should be 'Web Application.' Enter a name: I called mine DFP API Python.
Under the 'authorized Redirect URLs' section, enter a random URL.

<img width="671" alt="dfpcredentialstep4" src="https://cloud.githubusercontent.com/assets/17837150/22405587/f780702c-e5f9-11e6-8561-3be270258697.png">

When we are making a request to this API to generate our tokens, DFP will direct us to this URL which contains
the information we need.

When you are done, click Create and take note of your Client ID, Refresh URL, and Client Secret. We will need them in Step 2.


###Step 2 - Running Credentials script

Download the DFP API Python repo from Github and open it in a terminal window. To run the script from a terminal,
type "python generateToken" and press enter. Messages will be printed asking for:


    Refresh URI
    Client Secret
    Client ID

Copy and paste into the terminal and press enter to continue with script. At the end of the script, you will be
provided with a refresh token. Take this token, the Client ID, and the Client Secret and paste them into the
file named 'googleads.yaml' within the Credentials folder. You will need to open it in a text editor to do this.
Ensure you save the file. You do not need to run the generateToken script again, as the refresh token will stay
the same unless you refresh your client ID & Secret.


###Step 2b - Creating Values to associate with the hb_pb key

Step 2b involves creating values. The Key we associate to Prebid Bids, "hb_pb", must be set to 'predefined'
in DFP. In DFP, go to the inventory tab followed by Key-values. Search for hb_pb and make the values type:
'Users will select from predefined targeting values'.

If you haven't created the hb_pb key yet, do it now. After creating the Key, your url will contain the unique
key ID value:

    https://www.google.com/dfp/1234#inventory/customTargeting/keyId=12345678
    Make note of that keyId. You will need it when running the script.

When we create line items later on, a value ID must be specified for each line item's targeting. For example, a $10.00
line item with targeting hb_pb=10.00 must have that 10.00 value pre-defined in the system and given a unique ID.

Even if you have had Prebid running for a while, if your buckets have been setup at intervals larger than 1c you won't
have those values setup. Running the createValues script will fix that. If this isn't done, when we run the main script
it will throw errors when the valueID isn't defined.

'createValues' creates 1c values, starting at 0.01 and running up to the value you specify.
It will ask you to specify how many you want to create: 100 = 100 x 1c values. I suggest 15,000 which comes out to
$150 in 1c increments.

When you are ready simply type 'python createValues' followed by enter. Then input your key_id and number of values.

###Step 2b - Editing the script to include Ad Unit Sizes

Open the file 'createLineItem.py' in a text editor. On line 70, I have specified creative placeholder sizes as
a default. Work out what sizes your ad units are and fill this creativePlaceholders object with those sizes.
Be very careful to format it properly, with the exact same formatting as I have done just with your sizes instead
of mine. Also be careful not to include a comma after the final value as this will throw an error.

P.S. If you would line your line items to be called something different than "Prebid_", you can change that
name on line 28. Ensure you save the script after making changes.

###Step 3 - Plan Your Line Items

The main script will ask you for a number of inputs:

Order ID:
    You should have created your initial Prebid Order before running the script. You will also need to
    have created one line item at the same time. Make a note of what $ value this line item contains.

    Let's pretend you created the line item Prebid_0.01. This script will ask you what line item you first
    want to create, as well as the increments each line item increases by.
    With Prebid_0.01 already created, your starting amount should be 0.02 if incrementing in 1c amounts.
    Your starting amount should be 0.06 if incrementing in 5c amounts, and so on.

    Make sure you work out exactly which line item you want to start with, what increments you want, and the exact
    amount of line items you want to create at that increment.

    DFP has a maximum line item limit of 450 per order. So the maximum you can create per script is 449.

Ad Unit ID:
    You can find your Ad Unit IDs by going to the Inventory tab of DFP. Click on Ad Units in the sidebar
    and search for the ad units you want to use. The Ad Slot ID will be in the URL:

    https://www.google.com/dfp/1234#inventory/inventory/adSlotId=123456

    Please paste the ad unit IDs in the following format:

    1234567890,23456788,1234567890

Creative IDs:
    If you have never created a Prebid creative before, navigate to the following URL:
        http://prebid.org/adops/step-by-step.html#step-2-add-a-creative
    Navigate to the default Prebid line item you created above and create 1 third-party creative with
    the javascript snipped specified in Step 2 of prebid.org:

    <script>
            var w = window;
        for (i = 0; i < 10; i++) {
          w = w.parent;
          if (w.pbjs) {
            try {
              w.pbjs.renderAd(document, '%%PATTERN:hb_adid%%');
              break;
            } catch (e) {
              continue;
            }
          }
        }
    </script>

    You will need to create one of these creatives for each ad unit you plan on using. 6 ad units = 6 creatives.
    Ensure that you make each creative the size of the ad units you are targeting. Three 728x90 ad units =
    Three Prebid creatives size 720x90.

    Take note of each of these creative IDs, which can be found in the URL of each creative:
        https://www.google.com/dfp/123#delivery/PreviewCreative/orderId=1234&lineItemId=1234&creativeId=1234

    When the script asks you for these IDs, enter them in the following format:
        123456,123456,123456,123456

    You can skip the creation step if you already have creatives setup.

Key ID:
    The ID of your prebid hb_pb key. We collected this ID in Step 2b

Increment:
    Please ensure the increment value you specify is in decimal format:
        1c increment = 0.01
        10c increment is 0.1
        $1 increment is 1.00
        And so on.

Starting Amount:
    Please ensure this value is also a decimal.
        $1 starting value = 1.00
        1c starting value = 0.01

Number of Lines:
    The number of line items you want to create. This value can be a standard number, not a decimal.
    DFP has a line item limit of 449, plus the default line item you created.

Make sure you plan out your line items carefully. Create a dummy Order to practice on and try the script a few times.


###Step 4 - Run the main script

Simply type "python main" into the terminal, press enter, and input your information when you are prompted.
The script will run continuously until it is completed.

Please feel free to reach out with any questions, feedback, or requests.
