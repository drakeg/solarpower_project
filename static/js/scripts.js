// static/js/scripts.js

document.addEventListener('DOMContentLoaded', function () {
    const voteButtons = document.querySelectorAll('.upvote-btn, .downvote-btn');

    voteButtons.forEach(button => {
        button.addEventListener('click', () => {
            const responseId = button.getAttribute('data-response-id');
            const voteType = button.getAttribute('data-vote-type');
            voteResponse(responseId, voteType, button);
        });
    });

    function voteResponse(responseId, voteType, button) {
        const url = `/forum/vote_response/?response_id=${responseId}&vote_type=${voteType}`;
        
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),  // Get CSRF token from cookies
                'Content-Type': 'application/json',
            },
            // The body of the request remains the same
            body: JSON.stringify({ response_id: responseId, vote_type: voteType }),
        })
        .then(response => response.json())
        .then(data => {
            // ...
        })
        .catch(error => {
            // ...
        });
    }
    
    // Function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
