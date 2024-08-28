document.addEventListener("DOMContentLoaded", function() {
    var previewArea = document.getElementById('image-preview');
    var futuredImageUrl = previewArea.getAttribute('data-image-url');

    if (futuredImageUrl) {
        var uploadArea = document.getElementById('upload-container');
        previewArea.innerHTML = `
            <img src="${futuredImageUrl}" alt="Seçilen Resim">
            <button type="button" class="delete-btn" onclick="removeImage()">X</button>
        `;
        previewArea.style.display = 'block';
        uploadArea.style.display = 'none';
    }
});

// Dosya seçimini tetiklemek için
function triggerFileInput() {
    document.getElementById('futured_image').click();
}

// Dosya seçildiğinde önizleme yapma
function previewImage(event) {
    var file = event.target.files[0];
    var reader = new FileReader();
    reader.onload = function() {
        var previewArea = document.getElementById('image-preview');
        var uploadArea = document.getElementById('upload-container');
        previewArea.innerHTML = `
            <img src="${reader.result}" alt="Seçilen Resim">
            <button type="button" class="delete-btn" onclick="removeImage()">X</button>
        `;
        previewArea.style.display = 'block';  // Önizleme alanını göster
        uploadArea.style.display = 'none';    // Yükleme alanını gizle
    };
    reader.readAsDataURL(file);
}

// Resmi kaldırmak için
function removeImage() {
    var fileInput = document.getElementById('futured_image');
    fileInput.value = '';  // Dosya inputunu temizle
    var previewArea = document.getElementById('image-preview');
    var uploadArea = document.getElementById('upload-container');
    previewArea.style.display = 'none';  // Önizlemeyi gizle
    uploadArea.style.display = 'block';  // Yükleme alanını tekrar göster

    // Resmin kaldırıldığını backend'e bildirmek için ek bir hidden input ekleyebilirsiniz.
    document.getElementById('remove_image').value = 'true';
}