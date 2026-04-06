// ============================================
// CSRF Token Helper (reads from meta tag)
// ============================================
function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
}

// ============================================
// Side Panel (Buy Flow)
// ============================================
document.addEventListener("DOMContentLoaded", () => {
    const overlay   = document.getElementById("overlay");
    const sidePanel = document.getElementById("side-panel");
    const closeBtn  = document.getElementById("close-panel");

    const closeAll = () => {
        sidePanel.classList.remove("open");
        overlay.classList.remove("visible");
        setTimeout(() => { overlay.style.display = "none"; }, 350);
    };

    // Export so chat.js can call it
    window.openSidePanel = (contentHtml, footerHtml) => {
        document.getElementById("panel-content").innerHTML = contentHtml || '';
        document.getElementById("panel-footer").innerHTML  = footerHtml  || '';
        overlay.style.display = "block";
        requestAnimationFrame(() => {
            overlay.classList.add("visible");
            sidePanel.classList.add("open");
        });
    };

    if (overlay)  overlay.addEventListener("click", closeAll);
    if (closeBtn) closeBtn.addEventListener("click", closeAll);

    // ============================================
    // Products page — Buy Now buttons
    // ============================================
    document.querySelectorAll(".buy-now-btn").forEach(btn => {
        btn.addEventListener("click", () => openBuyPanel(
            btn.dataset.productId,
            btn.dataset.productName,
            btn.dataset.productPrice,
            btn.dataset.productImage
        ));
    });
});

// ============================================
// Shared Buy Panel Builder
// ============================================
function openBuyPanel(pid, name, price, image) {
    const contentHtml = `
        <div style="background:var(--surface-container-low);border-radius:var(--radius-2xl);padding:1.5rem;display:flex;gap:1.25rem;align-items:center;margin-bottom:2rem;">
            <img src="${image}" style="width:5rem;height:5rem;border-radius:var(--radius-lg);object-fit:cover;flex-shrink:0;" alt="${name}">
            <div>
                <p class="sku">SKU: ${String(pid).padStart(3,'0')}-HP</p>
                <h3 class="font-headline" style="font-weight:700;font-size:1rem;color:var(--on-surface);margin:0.25rem 0;">${name}</h3>
                <p style="font-family:var(--font-headline);font-weight:800;color:var(--primary);font-size:1.25rem;">&#x20B9;${price}</p>
            </div>
        </div>
        <div style="padding:0 0.25rem;">
            <div class="order-summary-item">
                <span style="color:var(--on-surface-variant);">Unit Price</span>
                <span style="font-weight:600;">&#x20B9;${price}</span>
            </div>
            <div class="order-summary-item" style="align-items:center;margin-bottom:1rem;">
                <span style="color:var(--on-surface-variant);">Quantity</span>
                <input type="number" id="buy-qty" class="qty-input" value="1" min="1" max="99">
            </div>
            <div class="order-summary-total">
                <span>Total</span>
                <span id="buy-subtotal">&#x20B9;${price}</span>
            </div>
        </div>
    `;

    const footerHtml = `
        <button class="btn btn-primary form-submit-btn" id="confirm-buy-btn" style="width:100%;padding:1rem;font-size:1rem;">
            <span class="material-symbols-outlined" style="font-size:1.25rem;">check_circle</span>
            Confirm Order
        </button>
    `;

    window.openSidePanel(contentHtml, footerHtml);

    // Subtotal live update
    const qtyInput = document.getElementById("buy-qty");
    qtyInput.addEventListener("input", () => {
        const qty = Math.max(1, parseInt(qtyInput.value) || 1);
        document.getElementById("buy-subtotal").textContent = `\u20B9${(parseFloat(price) * qty).toFixed(2)}`;
    });

    // Confirm order
    document.getElementById("confirm-buy-btn").addEventListener("click", () => {
        const qty = Math.max(1, parseInt(qtyInput.value) || 1);
        const btn = document.getElementById("confirm-buy-btn");
        btn.disabled = true;
        btn.textContent = "Processing...";

        fetch("/api/buy/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCsrfToken()
            },
            body: JSON.stringify({ product_id: pid, quantity: qty })
        })
        .then(res => res.json())
        .then(data => {
            if (data.message) {
                window.location.href = "/orders/";
            } else {
                alert("Error: " + (data.error || "Something went wrong."));
                btn.disabled = false;
                btn.innerHTML = `<span class="material-symbols-outlined">check_circle</span> Confirm Order`;
            }
        })
        .catch(() => {
            alert("Network error. Please try again.");
            btn.disabled = false;
            btn.innerHTML = `<span class="material-symbols-outlined">check_circle</span> Confirm Order`;
        });
    });
}
