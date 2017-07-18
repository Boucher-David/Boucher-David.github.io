pbjs.que.push(function() {
        pbjs.requestBids({
          timeout: PREBID_TIMEOUT,
          bidsBackHandler: function() {
            pbjs.setTargetingForGPTAsync();
            googletag.pubads().refresh();
          }
        });
      });
