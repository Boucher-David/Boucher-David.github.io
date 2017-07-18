chrome.runtime.sendMessage(chrome.runtime.id,
    {
      greeting: 'prebidBids',
      message: window.pbjs,
      timeout: PREBID_TIMEOUT
    }
);
