function filterCategory(category) {
    const productContainers = document.querySelectorAll('.product-container');

    productContainers.forEach(container => {
        if (category === 'all') {
            container.style.display = 'block';
        } else if (container.classList.contains(category)) {
            container.style.display = 'block';
        } else {
            container.style.display = 'none';
        }
    });
}
