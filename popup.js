// Define event handler function for saving URL
function saveURL() {
    var url = document.getElementById('urlInput').value;
    if (url) {
        fetch('http://127.0.0.1:5000/save_url', {
            method: 'POST',
            headers: {
                'Content-Type': 'text/plain' // Set Content-Type header to indicate plain text
            },
            body: url // Send the URL as plain text in the request body
        })
        .then(response => {
            if (response.ok) {
                console.log('URL saved successfully');
                // Trigger text analysis
                analyzeText();
            } else {
                console.error('Failed to save URL');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } else {
        console.error('URL is empty');
    }
}

// Define event handler function for text analysis
function analyzeText() {
    fetch('http://127.0.0.1:5000/analyse')
    .then(response => response.text())
    .then(data => {
        // Inject the HTML content into the page
        document.body.innerHTML = data;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Add event listener to button for saving URL
document.getElementById('saveButton').addEventListener('click', saveURL);
