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
                    console.log(results)
                    let no_outs = removeOutliers(results)
                    let no_out_data = no_outs.data
                    let num_removed = no_outs.outliersRemoved
                    let pct_out_removed = num_removed / results.length
                    
                    let sum = no_out_data.reduce((a, b) => a + parseFloat(b.replace("$", "")), 0);
                    let averagePrice = sum / no_out_data.length;
                    
                    document.getElementById("prices").textContent = "Average Price: $" + averagePrice.toFixed(2);
                    document.getElementById("outliers_removed_count").textContent = "Removed " + 
                        num_removed.toFixed(0) + " outliers. (" + formatAsPercentage(pct_out_removed) + ")";
                } else {
                    console.log("CONSOLE TEST")
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

function removeOutliers(data) {
    // Calculate the mean
    let mean = data.reduce((acc, val) => acc + val, 0) / data.length;

    // Calculate the standard deviation
    let squaredDiffs = data.map(val => Math.pow(val - mean, 2));
    let variance = squaredDiffs.reduce((acc, val) => acc + val, 0) / data.length;
    let stdDev = Math.sqrt(variance);

    // Filter out values that are outside 2 standard deviations from the mean
    let filteredData = data.filter(val => Math.abs(val - mean) <= 2 * stdDev);

    // Calculate the number of outliers removed
    let outliersRemoved = data.length - filteredData.length;

    console.log("Mean:", mean);
    console.log("Standard Deviation:", stdDev);
    console.log("Filtered data: ", filteredData);

    return {
        data: filteredData,
        outliersRemoved: outliersRemoved
    };
}

function formatAsPercentage(value) {
    let formatter = new Intl.NumberFormat('en-US', {
        style: 'percent',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    });

    return formatter.format(value);
}






