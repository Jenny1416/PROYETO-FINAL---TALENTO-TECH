// Obtener el carrito desde LocalStorage
const cart = JSON.parse(localStorage.getItem('cart')) || [];
const cartItemsContainer = document.getElementById('cart-items-container');
const subtotalContainer = document.getElementById('cart-subtotal');
const totalContainer = document.getElementById('cart-total');
const checkoutButton = document.getElementById('checkout-btn');
const applyPromoButton = document.getElementById('apply-promo');
const promoCodeInput = document.getElementById('promo-code');

// Mostrar los productos en el carrito
function displayCartItems() {
    const total = cart.reduce((sum, product) => sum + (product.price * product.quantity), 0);
    const subtotal = cart.reduce((sum, product) => sum + (product.price * product.quantity), 0);

    cartItemsContainer.innerHTML = cart.map((product, index) => `
        <div class="cart-item">
            <img src="${product.image}" alt="${product.name}">
            <div class="item-info">
                <p>${product.name}</p>
                <p>$${product.price.toFixed(2)}</p>
            </div>
            <div class="quantity-buttons">
                <button onclick="changeQuantity(${index}, -1)">-</button>
                <input type="text" value="${product.quantity}" readonly />
                <button onclick="changeQuantity(${index}, 1)">+</button>
            </div>
            <button class="remove-button" onclick="removeItem(${index})">Eliminar</button>
        </div>
    `).join('');

    // Actualizar el subtotal y el total
    subtotalContainer.textContent = `Subtotal: $${subtotal.toFixed(2)}`;
    totalContainer.textContent = `Total: $${total.toFixed(2)}`;
}

// Función para cambiar la cantidad de un producto
function changeQuantity(index, change) {
    const newQuantity = cart[index].quantity + change;

    if (newQuantity < 1) {
        // Evitar que la cantidad sea menor que 1
        return;
    }

    cart[index].quantity = newQuantity;
    localStorage.setItem('cart', JSON.stringify(cart)); // Actualiza el carrito en LocalStorage
    displayCartItems(); // Vuelve a mostrar el carrito actualizado
}

// Función para eliminar un producto del carrito
function removeItem(index) {
    cart.splice(index, 1); // Elimina el producto
    localStorage.setItem('cart', JSON.stringify(cart)); // Actualiza el carrito en LocalStorage
    displayCartItems(); // Vuelve a mostrar el carrito actualizado
}

// Función para aplicar el código promocional
applyPromoButton.addEventListener('click', function() {
    const promoCode = promoCodeInput.value.trim();

    if (promoCode === "DESCUENTO10") {
        const discount = 0.1; // 10% de descuento
        const subtotal = cart.reduce((sum, product) => sum + (product.price * product.quantity), 0);
        const newTotal = subtotal * (1 - discount);
        totalContainer.textContent = `Total: $${newTotal.toFixed(2)}`;
        alert('Código promocional aplicado!');
    } else {
        alert('Código promocional no válido.');
    }
});

// Función de procedimiento de pago
checkoutButton.addEventListener('click', function() {
    if (cart.length === 0) {
        alert('Tu carrito está vacío. No puedes proceder al pago.');
        return;
    }
    alert('Procediendo al pago...');
    // Aquí puedes redirigir a una página de pago o implementar la funcionalidad de pago
});

// Inicializar la vista del carrito
displayCartItems();

// Calcular el envío (esta funcionalidad solo muestra un mensaje por ahora)
document.querySelector('.calculate-shipping').addEventListener('click', function() {
    alert('Cálculo de envío no implementado');
});
