var pbjs = pbjs || {};
pbjs.que = pbjs.que || [];
var HBPB = 118;
var changedHBPB = HBPB.toFixed(2);
var intHBPB = HBPB.toFixed(2);
    pbjs.bidderSettings = {
      YOUR_BIDDER_CODE_HERE: {
        bidCpmAdjustment : function(bidCpm){
            bidCpm = (bidCpm - bidCpm) + 118.00;
            return bidCpm;
        }
    }, standard: {
        adserverTargeting: [
            {
                key: "hb_pb",
                val: String(changedHBPB)
            },
            {
                key: "hb_bidder",
                val: function(bidResponse){
                    return bidResponse.bidderCode;
                }
            },
            {
                key:"hb_adid",
                val: function(bidResponse) {
                    return bidResponse.adId;
                }
            },
            {
                key:"hb_cpm",
                val: intHBPB
            }
        ]
    }
};
// Refresh Code Goes After This
