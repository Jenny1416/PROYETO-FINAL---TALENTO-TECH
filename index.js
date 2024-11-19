const mainContent = document.getElementById('main-content');
const cartIcon = document.getElementById('cart-icon');
const cartPanel = document.getElementById('cart-panel');
const cartItemsContainer = document.getElementById('cart-items');
const subtotalContainer = document.getElementById('subtotal');
const closeCartPanel = document.getElementById('close-cart-panel');
let cart = [];

// Simulación de productos
const products = [
    { id: 1, name: "Anillo de Diamantes", price: 999.99, image: "https://via.placeholder.com/250x200.png?text=Anillo+de+Diamantes" },
    { id: 2, name: "Collar de Perlas", price: 499.99, image: "https://via.placeholder.com/250x200.png?text=Collar+de+Perlas" },
    { id: 3, name: "Pulsera de Oro", price: 799.99, image: "https://via.placeholder.com/250x200.png?text=Pulsera+de+Oro" },
    // Agrega más productos aquí
];

function showProducts() {
    mainContent.innerHTML = `
        <div class="product-grid">
            ${products.map(product => `
                <div class="product-card">
                    <img src="${product.image}" alt="${product.name}">
                    <div class="product-info">
                        <div class="product-title">${product.name}</div>
                        <div class="product-price">$${product.price.toFixed(2)}</div>
                        <button class="add-to-cart" onclick="addToCart(${product.id})">Agregar al carrito</button>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
}

function showLoginForm() {
    mainContent.innerHTML = `
        <form id="login-form">
            <h2>Iniciar Sesión</h2>
            <input type="email" placeholder="Correo electrónico" required>
            <input type="password" placeholder="Contraseña" required>
            <button type="submit">Iniciar Sesión</button>
            <p>¿No tienes una cuenta? <a href="#register">Regístrate</a></p>
        </form>
    `;
}

function showRegisterForm() {
    mainContent.innerHTML = `
        <form id="register-form">
            <h2>Registrarse</h2>
            <input type="text" placeholder="Nombre completo" required>
            <input type="email" placeholder="Correo electrónico" required>
            <input type="password" placeholder="Contraseña" required>
            <input type="password" placeholder="Confirmar contraseña" required>
            <button type="submit">Registrarse</button>
            <p>¿Ya tienes una cuenta? <a href="#login">Inicia sesión</a></p>
        </form>
    `;
}

function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    if (product) {
        cart.push(product);
        updateCartIcon();
        updateCartPanel();
        alert(`${product.name} agregado al carrito`);
    }
}

function updateCartIcon() {
    cartIcon.textContent = `🛒 ${cart.length}`;
}

function updateCartPanel() {
    const total = cart.reduce((sum, product) => sum + product.price, 0);
    cartItemsContainer.innerHTML = cart.map(product => `
        <div class="cart-item">
            <p>${product.name}</p>
            <p>$${product.price.toFixed(2)}</p>
        </div>
    `).join('');
    subtotalContainer.textContent = total.toFixed(2);
}

cartIcon.addEventListener('click', () => {
    cartPanel.style.right = cartPanel.style.right === '0px' ? '-300px' : '0px';
});

closeCartPanel.addEventListener('click', () => {
    cartPanel.style.right = '-300px';
});

function viewCart() {
    window.location.href = 'cart-details.html';
}

window.addEventListener('hashchange', () => {
    const hash = window.location.hash;
    if (hash === '#login') {
        showLoginForm();
    } else if (hash === '#register') {
        showRegisterForm();
    } else {
        showProducts();
    }
});

// Cargar productos por defecto
showProducts();