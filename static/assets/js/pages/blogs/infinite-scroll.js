let page = 2;
const container = document.getElementById('article-container');
const loading = document.getElementById('loading');
let loadingInProgress = false;
let hasNextPage = true;

window.onscroll = function() {
    if (!loadingInProgress && hasNextPage && (window.innerHeight + window.scrollY >= document.body.offsetHeight - 200)) {
        loadingInProgress = true;
        loading.style.display = 'none';

        const xhr = new XMLHttpRequest();
        xhr.open('GET', `?page=${page}`, true);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.onload = function() {
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                const div = document.createElement('div');
                div.innerHTML = response.article_list_html;
                while (div.firstChild) {
                    container.appendChild(div.firstChild);
                }
                hasNextPage = response.has_next;

                if (!hasNextPage) {
                    loading.style.display = 'none';

                    // "Daha fazla makale yok" uyarısını ekleme
                    const endMessage = document.createElement('p');
                    endMessage.textContent = 'Daha fazla makale yok';
                    endMessage.style.textAlign = 'center';
                    endMessage.style.marginTop = '20px';
                    container.appendChild(endMessage);
                } else {
                    loading.style.display = 'block';
                }

                loadingInProgress = false;
                page++;
            }
        };
        xhr.send();
    }
};
