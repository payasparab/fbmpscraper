document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("btnFetch").addEventListener("click", function() {
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            var tab = tabs[0];
            chrome.scripting.executeScript({
                target: {tabId: tab.id},
                func: fetchPricesFromHTML
            }, (injectionResults) => {
                let results = injectionResults[0].result;
                if (results && results.length) {
                    let sum = results.reduce((a, b) => a + parseFloat(b.replace("$", "")), 0);
                    let averagePrice = sum / results.length;
                    document.getElementById("prices").textContent = "Average Price: $" + averagePrice.toFixed(2);
                } else {
                    document.getElementById("prices").textContent = "No prices found!";
                }
            });
        });
    });
});

function fetchPricesFromHTML() {
    let regex = /\$\d{1,6}(\.\d{1,2})?/g;
    let html = document.documentElement.outerHTML;
    let matches = html.match(regex);
    return matches || [];
}





