    document.addEventListener('DOMContentLoaded', function() {
        let botones = document.querySelectorAll('.rating-button');
        let rateUrl = document.querySelector('#user-rating').dataset.rateUrl;
        console.log(rateUrl);
        botones.forEach(function(elem) {
            elem.addEventListener('click', function(event) {
                rateRestaurant(
                    rateUrl,
                    event.target.dataset.score
                );
            });
        });
    });

    function rateRestaurant(url, score) {
        let formData = new URLSearchParams();
        formData.append('score', score);

        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': '{{ csrf_token }}'
            }
        }).then((response) => {
            console.log(url, 'finished');
            console.log(response);
            if (response.ok) {
                console.log('Url succeeded with', response);
                location.reload();
            }
        }).catch((error) => {
            alert('Url failed with '+error+' '+url);
        })
    };