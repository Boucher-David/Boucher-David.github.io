function addJS(code) {
  var s = document.createElement("script");
  s.type="text/javascript";
  s.innerText = code;
  document.getElementsByTagName("body")[0].appendChild(s);
}

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    switch (request.greeting) {

      case "getPrebidResponses":
        addJS(`chrome.runtime.sendMessage('${chrome.runtime.id}',{greeting: 'prebidBids',message: window.pbjs, timeout: PREBID_TIMEOUT});`);
        break;

      case "refreshBids":
        addJS("pbjs.que.push(function() {pbjs.requestBids({timeout: window.PREBID_TIMEOUT,bidsBackHandler: function() {pbjs.setTargetingForGPTAsync();googletag.pubads().refresh();}});});");
        break;

      case "setTimeout":
        addJS(`PREBID_TIMEOUT = ${request.newTimeout}; var unitbids = window.pbjs.getHighestCpmBids(); chrome.runtime.sendMessage('${chrome.runtime.id}',{greeting: 'prebidTimeout', timeout: PREBID_TIMEOUT});`);
        break;

      case "setBidder":
        addJS(`var pbjs = pbjs || {};pbjs.que = pbjs.que || [];var HBPB = 118;var changedHBPB = HBPB.toFixed(2);var intHBPB = HBPB.toFixed(2);pbjs.bidderSettings = {${request.bidder}: {bidCpmAdjustment : function(bidCpm){bidCpm = (bidCpm - bidCpm) + 118.00;return bidCpm;}}, standard: {adserverTargeting: [{key: 'hb_pb',val: String(changedHBPB)},{key: 'hb_bidder',val: function(bidResponse){return bidResponse.bidderCode;}},{key:'hb_adid',val: function(bidResponse) {return bidResponse.adId;}},{key:'hb_cpm',val: intHBPB}]}};`);
        break;

      default:
        console.log("whoops, something goofed");
    }});
