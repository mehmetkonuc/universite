document.addEventListener("DOMContentLoaded", function() {
    var deleteModal = document.getElementById('deleteModal');
    var confirmDeleteBtn = document.getElementById('confirmDeleteBtn');

    function deleteComment() {
    // Her sil butonuna tıklanınca tetiklenecek
    document.querySelectorAll('.delete-post-btn').forEach(function(button) {
      button.addEventListener('click', function() {
        var commentId = this.getAttribute('data-id');
        var deleteUrl = '/comments/delete/' + commentId + '/'; // Silme URL'sini oluşturun
        confirmDeleteBtn.setAttribute('href', deleteUrl); // Modal'daki href'i güncelleyin
      });
    });
    };

    deleteComment(confirmDeleteBtn)

    const observer = new MutationObserver(mutations => {
        mutations.forEach(mutation => {
            if (mutation.addedNodes.length > 0) {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === 1 && node.matches('#confirmDeleteBtn')) {
                        deleteComment([node]);
                    } else if (node.nodeType === 1) {
                        const confirmDeleteBtn = node.querySelectorAll('#confirmDeleteBtn');
                        deleteComment(confirmDeleteBtn);
                    }
                });
            }
        });
    });

    // infinite-container içinde değişiklikleri izlemek için gözlemci başlat
    const config = { childList: true, subtree: true };
    const container = document.querySelector('.infinite-container');
    observer.observe(container, config);

});