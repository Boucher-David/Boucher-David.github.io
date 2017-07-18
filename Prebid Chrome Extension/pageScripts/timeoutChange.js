PREBID_TIMEOUT = YOUR_TIMEOUT;
chrome.runtime.sendMessage(chrome.runtime.id, {
  greeting: 'prebidTimeout',
  timeout: PREBID_TIMEOUT
});
