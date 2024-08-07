document.addEventListener('DOMContentLoaded', () => {
    const likeButtons = document.querySelectorAll('.like-btn');

    likeButtons.forEach(button => {
        button.addEventListener('click', () => {
            const contentTypeId = button.getAttribute('data-content-type-id');
            const objectId = button.getAttribute('data-object-id');
            const icon = button.querySelector('i');
            const likeCountSpan = button.querySelector('.like-count');

            fetch('/likes/like/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ content_type_id: contentTypeId, object_id: objectId }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.liked) {
                    icon.classList.add('ti-heart-filled');
                    icon.classList.remove('ti-heart');
                } else {
                    icon.classList.add('ti-heart');
                    icon.classList.remove('ti-heart-filled');
                }
                likeCountSpan.textContent = data.like_count;
            })
            .catch(error => console.error('Error:', error));
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
