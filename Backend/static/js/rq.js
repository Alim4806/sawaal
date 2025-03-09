document.getElementById("quit-btn").addEventListener("click", function() {
    if (confirm("Are you sure you want to quit Sawaal?")) {
        window.close(); // Attempt to close the window
    }
});
