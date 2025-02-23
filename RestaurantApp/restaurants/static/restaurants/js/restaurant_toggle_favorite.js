document.addEventListener('DOMContentLoaded', function() {
    let botones = document.querySelectorAll('.favorite');
    botones.forEach(function(elem) {
        elem.addEventListener('click', function(event) {
            let favUrl = event.currentTarget.dataset.favoriteUrl;
            toggleFavoriteRestaurant(favUrl, event.currentTarget);
        });
    });
});

function toggleFavoriteRestaurant(url, button) {
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.favorited) {
            button.classList.remove('fa-regular');
            button.classList.add('fa-solid', 'fa-bounce');
        } else {
            button.classList.remove('fa-solid', 'fa-bounce');
            button.classList.add('fa-regular');
        }
    }).catch((error) => {
        alert('Url failed with '+error+' '+url);
    })
};

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
