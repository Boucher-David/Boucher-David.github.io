chrome.runtime.onMessageExternal.addListener(function(request, sender, sendResponse) {
    var views = chrome.extension.getViews({
      type: "popup"
    })[0];
    if (request.greeting === "prebidBids") {
        chrome.runtime.sendMessage({greeting: "prebidBids", prebid: request.message, timeout: request.timeout});
    } else if (request.greeting === "prebidTimeout") {
        chrome.runtime.sendMessage({greeting: "setTimeout", timeout: request.timeout});
    }
});
