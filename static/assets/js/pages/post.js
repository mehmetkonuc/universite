/**
 * File Upload
 */

'use strict';

(function () {
  // previewTemplate: Updated Dropzone default previewTemplate
  // ! Don't change it unless you really know what you are doing
  const previewTemplate = `<div class="dz-preview dz-file-preview">
<div class="dz-details">
  <div class="dz-thumbnail">
    <img data-dz-thumbnail>
    <span class="dz-nopreview">No preview</span>
    <div class="dz-success-mark"></div>
    <div class="dz-error-mark"></div>
    <div class="dz-error-message"><span data-dz-errormessage></span></div>
    <div class="progress">
      <div class="progress-bar progress-bar-primary" role="progressbar" aria-valuemin="0" aria-valuemax="100" data-dz-uploadprogress></div>
    </div>
  </div>
  <div class="dz-filename" data-dz-name></div>
  <div class="dz-size" data-dz-size></div>
</div>
</div>`;

  // ? Start your code from here


  // Multiple Dropzone
  // --------------------------------------------------------------------
  const dropzoneMulti = document.querySelector('#dropzone-multi');
  if (dropzoneMulti) {
    const myDropzoneMulti = new Dropzone(dropzoneMulti, {
      previewTemplate: previewTemplate,
      parallelUploads: 1,
      maxFilesize: 5,
      addRemoveLinks: true
    });
  }
})();

document.addEventListener('DOMContentLoaded', () => {
  const likeButtons = document.querySelectorAll('.like-btn');

  likeButtons.forEach(button => {
      button.addEventListener('click', () => {
          const postId = button.getAttribute('data-post-id');
          const icon = button.querySelector('i');
          const likeCountSpan = button.querySelector('.like-count');

          fetch(`post/like/${postId}/`, {
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