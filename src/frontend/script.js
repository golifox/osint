/**
 * Обработчик клика для кнопки поиска. Запускает поиск по никнейму и отображает индикатор загрузки.
 */

document.getElementById('search-button').addEventListener('click', function () {
    const nickname = document.getElementById('nickname-input').value;
    toggleLoading(true);
    searchByNickname(nickname);
});

/**
 * Загружает категории с сервера и отображает их в виде кнопок в контейнере категорий.
 * Каждая категория представлена кнопками, соответствующими её ссылкам. Кнопки изначально неактивны.
 */
function loadCategories() {
    const apiUrl = 'http://0.0.0.0:8000';

    fetch(`${apiUrl}/api/categories/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(categories => {
            const categoriesContainer = document.getElementById('categories-container');
            categoriesContainer.innerHTML = '';

            categories.forEach(category => {
                const categoryDiv = document.createElement('div');
                categoryDiv.className = 'category-container mb-3';
                const tableDiv = document.createElement('div');
                tableDiv.className = 'category-table';

                category.links.forEach(link => {
                    const button = document.createElement('button');
                    button.className = 'category-button btn btn-light';
                    button.innerText = link.name;
                    button.disabled = true;

                    tableDiv.appendChild(button);
                });

                categoryDiv.appendChild(tableDiv);
                categoriesContainer.appendChild(categoryDiv);
            });
        })
        .catch(error => {
            console.error('Error loading categories:', error);
        });
}

/**
 * Переключает отображение индикатора загрузки в зависимости от состояния загрузки.
 *
 * @param {boolean} isLoading - Флаг состояния загрузки.
 */
function toggleLoading(isLoading) {
    document.getElementById('loading').style.display = isLoading ? 'block' : 'none';
}

/**
 * Выполняет поиск по никнейму и обновляет интерфейс на основе результатов поиска.
 * Активирует кнопки, соответствующие найденным ссылкам, и добавляет кликабельные ссылки.
 *
 * @param {string} nickname - Никнейм, по которому выполняется поиск.
 */
function searchByNickname(nickname) {
    const apiUrl = 'http://0.0.0.0:8000';

    fetch(`${apiUrl}/api/search`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({nickname: nickname, category_ids: []})
    })
        .then(response => response.json())
        .then(data => {
            toggleLoading(false);
            highlightFoundLinks(data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

/**
 * Обновляет кнопки на основе результатов поиска.
 * Кнопки, соответствующие найденным ссылкам, становятся зелеными и кликабельными.
 *
 * @param {Array} searchResults - Результаты поиска для обновления кнопок.
 */
function highlightFoundLinks(searchResults) {
    const buttons = document.querySelectorAll('.category-button');

    buttons.forEach(button => {
        const result = searchResults.find(result => result.link.name === button.innerText);

        if (result && result.found) {
            button.classList.add('found');
            button.disabled = false;

            if (result.found_link) {
                const link = document.createElement('a');
                link.href = result.found_link;
                link.target = '_blank';
                link.classList.add('category-link');
                link.appendChild(button.cloneNode(true));
                button.parentNode.replaceChild(link, button);
            }
        }
    });
}


window.onload = loadCategories;
