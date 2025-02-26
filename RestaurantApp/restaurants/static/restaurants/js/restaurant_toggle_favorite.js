document.getElementById('restaurants_list').addEventListener('click', function(event) {
    let button = event.target.closest('.favorite');
    if (button) {
        let favUrl = button.dataset.favoriteUrl;
        toggleFavoriteRestaurant(favUrl, button);
    }
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
