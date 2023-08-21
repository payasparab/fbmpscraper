document.addEventListener('DOMContentLoaded', function() {
    chrome.tabs.executeScript({
        code: 'document.documentElement.outerHTML'
    }, function(selection) {
        const htmlContent = selection[0];
        
        // Extracting prices from the HTML
        const regex = /\$\d{1,6}(\.\d{1,2})?/g;
        const matches = htmlContent.match(regex);
        
        // Displaying the extracted prices in the popup (for now, as a simple list)
        let priceList = '';
        matches.forEach(price => {
            priceList += `<li>${price}</li>`;
        });
        document.getElementById('prices').innerHTML = `<ul>${priceList}</ul>`;
    });
});





