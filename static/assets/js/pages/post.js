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
    const form = document.getElementById('post-form');
    form.addEventListener('submit', function() {
        updateFileInput();
    });
});
