document.addEventListener('DOMContentLoaded', function() {
    const ordersContainer = document.getElementById('orders-container');

    // Simular la carga de datos desde LocalStorage (si no hay, inicializa un array vacío)
    const orders = JSON.parse(localStorage.getItem('orders')) || [];

    if (orders.length === 0) {
        ordersContainer.innerHTML = '<p>No tienes órdenes realizadas aún.</p>';
    } else {
        // Mostrar las órdenes almacenadas
        orders.forEach(order => {
            const orderCard = document.createElement('div');
            orderCard.classList.add('order-card');

            // Mostrar detalles de cada orden
            orderCard.innerHTML = `
                <h3>Orden #${order.orderNumber}</h3>
                <div class="order-details">
                    <p><strong>Fecha:</strong> ${new Date(order.date).toLocaleDateString()}</p>
                    <p><strong>Subtotal:</strong> $${order.subtotal.toFixed(2)}</p>
                    <p><strong>Costo de Envío:</strong> $${order.shippingCost.toFixed(2)}</p>
                    <p><strong>Total:</strong> $${order.total.toFixed(2)}</p>
                    <p><strong>Estado:</strong> <span class="order-status ${order.status}">${order.status}</span></p>
                </div>
            `;

            ordersContainer.appendChild(orderCard);
        });
    }
});
