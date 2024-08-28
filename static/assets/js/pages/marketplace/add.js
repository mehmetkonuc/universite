document.addEventListener("DOMContentLoaded", function() {
    var previewsArea = document.getElementById('image-previews');
    var hasImages = previewsArea.querySelectorAll('.image-preview[data-image-url]').length > 0;
    
    if (hasImages) {
        previewsArea.style.display = 'flex';
    }
});

// Dosya seçimini tetiklemek için
function triggerFileInput() {
    document.getElementById('images').click();
}

// Dosya seçildiğinde önizleme yapma
function previewImages(event) {
    var files = event.target.files;
    var previewsArea = document.getElementById('image-previews');
    var uploadContainer = document.getElementById('upload-container');
    
    // Dosyaları döngüye alarak her bir dosya için önizleme oluştur
    Array.from(files).forEach(function(file) {
        var reader = new FileReader();
        reader.onload = function() {
            var previewDiv = document.createElement('div');
            previewDiv.className = 'image-preview';
            previewDiv.innerHTML = `
                <img src="${reader.result}" alt="Seçilen Resim">
                <button type="button" class="delete-btn" onclick="removeImage(this)">X</button>
            `;
            previewsArea.appendChild(previewDiv);
        };
        reader.readAsDataURL(file);
    });

    // Yeni resim yükleme butonunu ekle, eğer mevcut değilse
    if (!document.querySelector('.upload-icon-area')) {
        var addIconDiv = document.createElement('div');
        addIconDiv.className = 'image-preview';
        addIconDiv.innerHTML = `
            <div class="upload-icon-area" onclick="triggerFileInput()">
                <i class="ti ti-plus ti-32px mb-4"></i>
            </div>
        `;
        previewsArea.appendChild(addIconDiv);
    }

    // Görünürlüğü güncelle
    previewsArea.style.display = 'flex';
    uploadContainer.style.display = 'none';
}

// Resmi kaldırmak için
function removeImage(button) {
    var previewDiv = button.parentElement;
    previewDiv.remove();

    // Eğer tüm resimler kaldırıldıysa, yükleme alanını tekrar göster
    var previewsArea = document.getElementById('image-previews');
    var uploadContainer = document.getElementById('upload-container');
    
    if (previewsArea.children.length === 1) {
        previewsArea.style.display = 'none';
        uploadContainer.style.display = 'block';
    }
}
