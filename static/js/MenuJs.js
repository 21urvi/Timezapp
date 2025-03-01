function toggleMenu() {
    const menuItems = document.getElementById('menu-items');
    menuItems.classList.toggle('hidden');
}

function closeMenu() {
    window.location.href = '/'; // Adjust the path as needed to redirect to your home page
}
