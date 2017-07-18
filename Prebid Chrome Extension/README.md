### Before You install

You must first edit the manifest.json file to include the websites you want to capture bids from.

```javascript
"externally_connectable": {
  "matches": ["*://*.*****.*****/*"],
  "ids": ["*"]
}
```

Simply put your URL in the above matches entry within the manifest.json file. Then load the unpacked extension.

## Full Discretion

To grab prebid information, I have to inject a script to the body of your webpage. I am injecting this code from the contentScript.js file. The function addJS simply takes a bunch of code, complete with your desired timeout or bidder, and puts it on the page.

Please feel free to check out the pageScripts folder, which has each of these code snippets arranged in a nice way so you know exactly what is going on at all times. Reach out if you have any other questions.
