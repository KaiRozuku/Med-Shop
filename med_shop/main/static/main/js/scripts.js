document.addEventListener('DOMContentLoaded', function() {
    const filterButton = document.querySelector('.filter-button');
    const filterMenu = document.querySelector('.filter');

    document.querySelector('.filter-button').addEventListener('click', function() {
        document.querySelector('.filter').classList.toggle('open');
    });
});
