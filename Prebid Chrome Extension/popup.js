function setCookie(name, value){
  var d = new Date();
  d.setTime(d.getTime() + (1*24*60*60*1000));
  var expires = `expires=${d.toUTCString()}`;
  document.cookie = `${name}=${value};${expires};path=/`;
  console.log(`${name}=${value};${expires};path=/`);
};

function getCookie(cookieName){
  let name = `${cookieName}=`;
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(";");
  for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return false;
};

chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
  chrome.tabs.sendMessage(tabs[0].id, {greeting: "getPrebidResponses"}, function(response) {
  });
});

$("button").click((e) => {

  switch (e.target.id) {
    case "refreshBids":
      chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {greeting: "refreshBids"}, function(response) {
        });
      });
      break;

    case "timeoutButton":
      if (isNaN($("#newTimeout").val())) {
        $("#newTimeout").val("Please enter a number");
      } else {
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
          chrome.tabs.sendMessage(tabs[0].id, {greeting: "setTimeout", newTimeout: $("#newTimeout").val()}, function(response) {
          });
        });
        $("#currentTimeout").html("Current Prebid Timeout Is: " + $("#newTimeout").val());
      }
      break;

    case "bidderButton":
      var bidder = $("#bidderCode").val();
      chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {greeting: "setBidder", bidder: bidder}, function(response) {
        });
      });
      break;

    default:
      console.log("didn't work");
  }
});

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {

  if (request.greeting === "prebidBids") {
    $("#currentTimeout").html("Current Prebid Timeout Is: " + request.timeout);
    var winningID = [];

    if (request.prebid._winningBids.length > 0) {
      $.each(request.prebid._winningBids, function(index, value) {
        winningID.push(value.adId);
      })
    }

    $.each(request.prebid._bidsReceived, function(index, value) {
      if (request.timeout >= value.timeToRespond) {
        let winningRow;
        let bidSubmitted;
        (getCookie(value.adId)) ? bidSubmitted = `<td id='wonTrue'>Yes</td>` : bidSubmitted = `<td id='wonFalse'>No</td>`;
        (winningID.indexOf(value.adId) !== -1) ? winningRow = "<td id='wonTrue'>Yes</td>" : winningRow = "<td id='wonFalse'>No</td>";

        let auctionRow = `<tr><td>${value.adId}</td><td>${value.bidder}</td><td>${Number(value.cpm).toFixed(2)}</td><td>${value.timeToRespond}ms</td><td>${value.adUnitCode}</td>${bidSubmitted}${winningRow}</tr>`;
        $("#tableFoot").append(auctionRow);
      }
    });
  }
});

chrome.webRequest.onHeadersReceived.addListener(function(e) {
  if ((e.url).search("gampad/ads") != -1) {
    var fixedURL = (e.url).replace(/%3D/g, '=').replace(/%26/g, '&').match(/hb_adid=([^&]*)/);
    if (fixedURL !== null) {
      setCookie(fixedURL[1], fixedURL[1]);
    }
  }

}, {
  urls: ["<all_urls>"],
  types: ["script"]
});
