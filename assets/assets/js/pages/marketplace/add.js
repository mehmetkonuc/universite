document.addEventListener("DOMContentLoaded", function() {
    var previewsArea = document.getElementById('image-previews');
    var uploadContainer = document.getElementById('upload-container');

    // Daha önce yüklenmiş resimler varsa, upload-container gizlenmeli ve addIconDiv görünmeli
    if (previewsArea.querySelectorAll('.image-preview').length > 0) {
        previewsArea.style.display = 'flex';
        uploadContainer.style.display = 'none';
        showAddIconDiv(previewsArea);
    }

    // Dosya seçimini tetiklemek için tıklama olayı ekleniyor
    uploadContainer.addEventListener('click', function() {
        document.getElementById('images').click();
    });
});

// Seçilen dosyaları takip eden array
var selectedFiles = [];

// Yeni dosya seçildiğinde önizleme yapma
function previewImages(event) {
    var files = Array.from(event.target.files);
    var previewsArea = document.getElementById('image-previews');
    var uploadContainer = document.getElementById('upload-container');

    files.forEach(function(file) {
        selectedFiles.push(file);

        var reader = new FileReader();
        reader.onload = function() {
            var previewDiv = document.createElement('div');
            previewDiv.className = 'image-preview';
            previewDiv.innerHTML = `
                <img src="${reader.result}" alt="Seçilen Resim">
                <button type="button" class="delete-btn" onclick="removeImage(this, '${file.name}')">X</button>
            `;
            previewsArea.appendChild(previewDiv);
        };
        reader.readAsDataURL(file);
    });

    uploadContainer.style.display = 'none';
    previewsArea.style.display = 'flex';
    
    showAddIconDiv(previewsArea);
}

// addIconDiv'i gösteren fonksiyon
function showAddIconDiv(previewsArea) {
    if (!previewsArea.querySelector('.upload-icon-area')) {
        var addIconDiv = document.createElement('div');
        addIconDiv.className = 'image-preview';
        addIconDiv.innerHTML = `
            <div class="upload-icon-area">
                <i class="ti ti-plus ti-32px mb-4"></i>
            </div>
        `;
        previewsArea.insertBefore(addIconDiv, previewsArea.firstChild);

        // addIconDiv'e tıklama olayı ekleniyor
        addIconDiv.addEventListener('click', function() {
            document.getElementById('images').click();
        });
    }
}

function removeImage(button, fileName) {
    var previewDiv = button.parentElement;
    var previewsArea = document.getElementById('image-previews');
    var uploadContainer = document.getElementById('upload-container');
    var imageId = previewDiv.dataset.imageId;
    var deletedImagesInput = document.getElementById('deleted-images');

    // Önizleme div'ini kaldır
    previewDiv.remove();

    // selectedFiles array'inden dosyayı kaldır (sadece yeni eklenen dosyalar için)
    if (fileName) {
        selectedFiles = selectedFiles.filter(function(file) {
            return file.name !== fileName;
        });
    }

    // Resim ID'sini saklama (silinen resim ID'lerini saklamak için)
    if (imageId) {
        var currentValue = deletedImagesInput.value;
        deletedImagesInput.value = currentValue ? currentValue + ',' + imageId : imageId;
    }

    // Görünüm güncelleme
    if (previewsArea.querySelectorAll('.image-preview').length === 1) {  // Sadece addIconDiv kalmışsa
        previewsArea.style.display = 'none';
        uploadContainer.style.display = 'block';
    }
}

// Form gönderildiğinde seçilen dosyaları input elementine ekleme
document.querySelector('form').addEventListener('submit', function(event) {
    var inputElement = document.getElementById('images');
    var dataTransfer = new DataTransfer();

    selectedFiles.forEach(function(file) {
        dataTransfer.items.add(file);
    });

    inputElement.files = dataTransfer.files;

    // selectedFiles dizisini temizle
    selectedFiles = [];
});