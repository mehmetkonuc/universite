/**
 * File Upload
 */

'use strict';

document.addEventListener('DOMContentLoaded', () => {
    const likeButtons = document.querySelectorAll('.like-comment-btn');

    likeButtons.forEach(button => {
        button.addEventListener('click', () => {
            const commentId = button.getAttribute('data-comment-id');
            const icon = button.querySelector('i');
            const likeCountSpan = button.querySelector('.like-comment-count');

            fetch(`/post/like-comment/${commentId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ comment_id: commentId }),
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

document.addEventListener('DOMContentLoaded', () => {
    const likeButtons = document.querySelectorAll('.like-btn');

    likeButtons.forEach(button => {
        button.addEventListener('click', () => {
            const postId = button.getAttribute('data-post-id');
            const icon = button.querySelector('i');
            const likeCountSpan = button.querySelector('.like-count');

            fetch(`/post/like/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ post_id: postId }),
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

document.addEventListener("DOMContentLoaded", function() {
    const previewContainer = document.getElementById('preview-container');
    const fileInput = document.getElementById('id_images');
    const maxImages = 4;
    let existingFiles = [];  // Saklamak için bir dizi

    fileInput.addEventListener('change', function(event) {
        const files = Array.from(event.target.files);

        // Yeni dosyalar mevcut dosyalarla birleştirilir
        const newFiles = files.filter(file => !existingFiles.some(existingFile => existingFile.name === file.name));
        if (newFiles.length + existingFiles.length > maxImages) {
            alert(`Maksimum ${maxImages} resim yükleyebilirsiniz.`);
            return;
        }

        existingFiles = existingFiles.concat(newFiles);

        // Mevcut thumbnail'ları temizle
        previewContainer.innerHTML = '';

        existingFiles.forEach(file => {
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();

                reader.onload = function(e) {
                    // Thumbnail container
                    const div = document.createElement('div');
                    div.classList.add('thumbnail-container');
                    
                    // Thumbnail image
                    const img = document.createElement('img');
                    img.src = e.target.result;
                    div.appendChild(img);

                    // Remove button
                    const removeButton = document.createElement('button');
                    removeButton.textContent = 'x';
                    removeButton.classList.add('remove-button');
                    removeButton.onclick = function() {
                        // Silme işlemi
                        previewContainer.removeChild(div);
                        existingFiles = existingFiles.filter(existingFile => existingFile.name !== file.name);

                        // File input'ı güncelle
                        updateFileInput();
                    };
                    div.appendChild(removeButton);

                    previewContainer.appendChild(div);
                };

                reader.readAsDataURL(file);
            }
        });
    });

    // File input'ı güncelleme işlevi
    function updateFileInput() {
        const dataTransfer = new DataTransfer();
        existingFiles.forEach(file => dataTransfer.items.add(file));
        fileInput.files = dataTransfer.files;
    }

    // Form gönderiminde dosyaları güncelleme
    const form = document.getElementById('comment-form');
    form.addEventListener('submit', function() {
        updateFileInput();
    });
});
