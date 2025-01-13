// cart.js
window.onload = function() {
    // Initialize cart items from backend
    fetch('/get-cart-items')
        .then(response => response.json())
        .then(data => {
            if (data.cart && data.cart.length > 0) {
                displayCartItems(data.cart);
            } else {
                document.getElementById('empty-cart-message').style.display = 'block';
            }
        });

    // Handle checkout click
    document.getElementById('checkout-button').addEventListener('click', function() {
        window.location.href = '/checkout';
    });
};

// Function to display cart items
function displayCartItems(cart) {
    const cartItemsContainer = document.getElementById('cart-items');
    cartItemsContainer.innerHTML = ''; // Clear existing items
    let totalPrice = 0;

    cart.forEach(item => {
        totalPrice += item.price * item.quantity;

        const cartItem = document.createElement('div');
        cartItem.classList.add('cart-item');
        cartItem.innerHTML = `
            <img src="${item.image}" alt="${item.name}" class="cart-item-image">
            <div class="cart-item-details">
                <h3>${item.name}</h3>
                <p>Price: $${item.price}</p>
                <div class="quantity-control">
                    <button class="decrease" data-id="${item.id}">-</button>
                    <input type="number" class="quantity" value="${item.quantity}" min="1" data-id="${item.id}">
                    <button class="increase" data-id="${item.id}">+</button>
                </div>
                <button class="remove-item" data-id="${item.id}">Remove</button>
            </div>
        `;
        cartItemsContainer.appendChild(cartItem);
    });

    document.getElementById('total-price').innerText = totalPrice.toFixed(2);
    document.getElementById('cart-summary').style.display = 'block';

    // Add event listeners for quantity changes and item removal
    document.querySelectorAll('.increase').forEach(button => {
        button.addEventListener('click', increaseQuantity);
    });
    document.querySelectorAll('.decrease').forEach(button => {
        button.addEventListener('click', decreaseQuantity);
    });
    document.querySelectorAll('.remove-item').forEach(button => {
        button.addEventListener('click', removeItem);
    });
}

// Function to increase the quantity
function increaseQuantity(e) {
    const itemId = e.target.getAttribute('data-id');
    updateCartItemQuantity(itemId, 1);
}

// Function to decrease the quantity
function decreaseQuantity(e) {
    const itemId = e.target.getAttribute('data-id');
    updateCartItemQuantity(itemId, -1);
}

// Function to update item quantity
function updateCartItemQuantity(itemId, change) {
    fetch(`/update-cart-item/${itemId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ change })
    })
    .then(response => response.json())
    .then(data => {
        displayCartItems(data.cart);
    });
}

// Function to remove item
function removeItem(e) {
    const itemId = e.target.getAttribute('data-id');
    fetch(`/remove-from-cart/${itemId}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        displayCartItems(data.cart);
    });
}
