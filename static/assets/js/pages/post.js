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
