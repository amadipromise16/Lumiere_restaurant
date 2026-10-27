// Lumière Fine Dining - Main JavaScript

// Mobile Navigation Toggle
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('mobile-menu-button');
    const menu = document.getElementById('mobile-menu');
    if (btn && menu) {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            menu.classList.toggle('hidden');
        });
        document.addEventListener('click', (e) => {
            if (!menu.contains(e.target) && !btn.contains(e.target) && !menu.classList.contains('hidden')) {
                menu.classList.add('hidden');
            }
        });
    }

    // Auto-dismiss flash notifications after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            msg.style.opacity = '0';
            msg.style.transform = 'translateY(-10px)';
            setTimeout(() => msg.remove(), 600);
        }, 5000);
    });

    // Initialize Cart UI
    updateCartUI();

    // Menu Featured Carousel
    initCarousel();
});

// Carousel Logic for Menu Page
let carouselInterval = null;
function initCarousel() {
    const slides = document.querySelectorAll('.carousel-slide');
    if (!slides || slides.length === 0) return;

    let currentSlide = 0;
    const changeSlide = () => {
        slides[currentSlide].classList.remove('opacity-100', 'z-10');
        slides[currentSlide].classList.add('opacity-0', 'z-0');
        currentSlide = (currentSlide + 1) % slides.length;
        slides[currentSlide].classList.remove('opacity-0', 'z-0');
        slides[currentSlide].classList.add('opacity-100', 'z-10');
    };

    carouselInterval = setInterval(changeSlide, 3500);

    const carouselContainer = document.querySelector('.carousel-container');
    if (carouselContainer) {
        carouselContainer.addEventListener('mouseenter', () => clearInterval(carouselInterval));
        carouselContainer.addEventListener('mouseleave', () => {
            clearInterval(carouselInterval);
            carouselInterval = setInterval(changeSlide, 3500);
        });
    }
}

// Global Cart Functionality
let cart = JSON.parse(localStorage.getItem('lumiere_cart')) || [];

function saveCart() {
    localStorage.setItem('lumiere_cart', JSON.stringify(cart));
    updateCartUI();
}

function addToCart(id, name, price, image) {
    const itemId = String(id);
    const existing = cart.find(item => String(item.id) === itemId);
    if (existing) {
        existing.quantity += 1;
    } else {
        cart.push({ id: itemId, name: name, price: parseFloat(price), image: image, quantity: 1 });
    }
    saveCart();
    toggleCartSidebar(true);

    // Toast feedback
    showToast(`Added "${name}" to your order.`);
}

function updateQuantity(id, change) {
    const itemId = String(id);
    const item = cart.find(i => String(i.id) === itemId);
    if (item) {
        item.quantity += change;
        if (item.quantity <= 0) {
            cart = cart.filter(i => String(i.id) !== itemId);
        }
    }
    saveCart();
}

function removeFromCart(id) {
    const itemId = String(id);
    cart = cart.filter(i => String(i.id) !== itemId);
    saveCart();
}

function toggleCartSidebar(forceOpen = null) {
    const sidebar = document.getElementById('cart-sidebar');
    const overlay = document.getElementById('cart-sidebar-overlay');
    if (!sidebar || !overlay) return;

    if (forceOpen === true) {
        sidebar.classList.remove('translate-x-full');
        overlay.classList.remove('hidden');
    } else if (forceOpen === false) {
        sidebar.classList.add('translate-x-full');
        overlay.classList.add('hidden');
    } else {
        sidebar.classList.toggle('translate-x-full');
        overlay.classList.toggle('hidden');
    }
}

function updateCartUI() {
    const container = document.getElementById('cart-items-container');
    const badge = document.getElementById('cart-badge');
    const headerCount = document.getElementById('cart-count-header');
    const subtotalEl = document.getElementById('cart-subtotal');
    const serviceEl = document.getElementById('cart-service');
    const totalEl = document.getElementById('cart-total');

    const totalItems = cart.reduce((sum, i) => sum + i.quantity, 0);
    if (badge) {
        badge.innerText = totalItems;
        badge.style.display = totalItems > 0 ? 'flex' : 'none';
    }
    if (headerCount) headerCount.innerText = totalItems;

    if (!container) return;

    if (cart.length === 0) {
        container.innerHTML = `
            <div class="text-center py-12">
                <i class="fa-solid fa-basket-shopping text-neutral-300 text-4xl mb-3"></i>
                <p class="text-xs uppercase tracking-wider text-neutral-500 font-medium">Your cart is currently empty</p>
                <p class="text-[11px] text-neutral-400 mt-1">Explore our curated menu and add exquisite dishes.</p>
            </div>
        `;
        if (subtotalEl) subtotalEl.innerText = '$0.00';
        if (serviceEl) serviceEl.innerText = '$0.00';
        if (totalEl) totalEl.innerText = '$0.00';
        return;
    }

    let html = '';
    let subtotal = 0;

    cart.forEach(item => {
        subtotal += item.price * item.quantity;
        html += `
            <div class="flex items-center gap-3 bg-white p-3 rounded-sm shadow-xs border border-amber-900/10">
                <img src="${item.image}" alt="${item.name}" class="w-16 h-16 object-cover rounded-sm border border-neutral-200">
                <div class="flex-grow min-w-0">
                    <h4 class="font-serif font-bold text-burgundy text-sm truncate">${item.name}</h4>
                    <p class="text-xs text-gold font-semibold">$${item.price.toFixed(2)}</p>
                    <div class="flex items-center gap-2 mt-2">
                        <button onclick="updateQuantity('${item.id}', -1)" class="w-5 h-5 bg-cream border border-neutral-300 text-burgundy rounded flex items-center justify-center text-xs hover:bg-neutral-200">-</button>
                        <span class="text-xs font-semibold px-1">${item.quantity}</span>
                        <button onclick="updateQuantity('${item.id}', 1)" class="w-5 h-5 bg-cream border border-neutral-300 text-burgundy rounded flex items-center justify-center text-xs hover:bg-neutral-200">+</button>
                    </div>
                </div>
                <div class="text-right">
                    <p class="text-xs font-serif font-bold text-burgundy">$${(item.price * item.quantity).toFixed(2)}</p>
                    <button onclick="removeFromCart('${item.id}')" class="text-neutral-400 hover:text-red-600 p-1 text-xs mt-2" title="Remove item">
                        <i class="fa-solid fa-trash-can"></i>
                    </button>
                </div>
            </div>
        `;
    });

    container.innerHTML = html;
    const service = subtotal > 0 ? 5.00 : 0.00;
    const total = subtotal + service;

    if (subtotalEl) subtotalEl.innerText = `$${subtotal.toFixed(2)}`;
    if (serviceEl) serviceEl.innerText = `$${service.toFixed(2)}`;
    if (totalEl) totalEl.innerText = `$${total.toFixed(2)}`;
}

function checkoutCart() {
    if (cart.length === 0) {
        alert('Your cart is empty. Please select dishes from the menu first.');
        return;
    }
    const orderNumber = 'LMR-' + Math.floor(100000 + Math.random() * 900000);
    showToast(`Order #${orderNumber} placed successfully! Thank you for dining with Lumière.`);
    cart = [];
    saveCart();
    setTimeout(() => toggleCartSidebar(false), 1200);
}

// Like Card Heart Toggle
function toggleCardLike(btn) {
    const icon = btn.querySelector('i');
    if (!icon) return;
    if (icon.classList.contains('fa-regular')) {
        icon.classList.remove('fa-regular');
        icon.classList.add('fa-solid');
        icon.style.color = '#4A1C2B';
    } else {
        icon.classList.remove('fa-solid');
        icon.classList.add('fa-regular');
        icon.style.color = '';
    }
}

// Simple Toast Notification
function showToast(message) {
    let toast = document.getElementById('lumiere-toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'lumiere-toast';
        toast.className = 'fixed bottom-6 left-6 z-50 bg-[#1A1A1A] text-white px-5 py-3 rounded shadow-2xl text-xs uppercase tracking-wider font-medium border-l-4 border-gold transition-all duration-300 flex items-center gap-2';
        document.body.appendChild(toast);
    }
    toast.innerHTML = `<i class="fa-solid fa-bell text-gold"></i> ${message}`;
    toast.style.opacity = '1';
    toast.style.transform = 'translateY(0)';
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
    }, 4000);
}