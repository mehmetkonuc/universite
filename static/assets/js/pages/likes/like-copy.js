/**
 * File Upload
 */

'use strict';

document.addEventListener('DOMContentLoaded', () => {
    // const likeContainer = document.querySelector('.infinite-container'); // Change this selector to the closest parent element that exists when the page loads

    // likeContainer.addEventListener('click', (event) => {
    //     const likeButtons = document.querySelectorAll('.like-btn');

    // });
        const likeButtons = document.querySelectorAll('.like-btn');

        likeButtons.forEach(button => {
            button.addEventListener('click', () => {
                const contentTypeId = button.getAttribute('data-content-type-id');
                const objectId = button.getAttribute('data-object-id');
                const icon = button.querySelector('i');
                const likeCountSpan = button.querySelector('.like-count');
                console.log(contentTypeId)
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
                        likeCountSpan.textContent = 'Beğendin (' + data.like_count + ')';

                    } else {
                        icon.classList.add('ti-heart');
                        icon.classList.remove('ti-heart-filled');
                        likeCountSpan.textContent = 'Beğen (' + data.like_count + ')';
                    }

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
