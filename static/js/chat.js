// ============================================
// Chatbot — AJAX Chat Interface
// NOTE: main.js must be loaded before this file.
// ============================================
document.addEventListener("DOMContentLoaded", () => {
    const chatBox   = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn   = document.getElementById("send-btn");

    if (!chatBox) return; // Only run on the home/chat page

    // ----------------------------------------
    // Helper: Append a message bubble
    // ----------------------------------------
    const addMessage = (text, isBot = true, products = []) => {
        const wrap = document.createElement("div");
        wrap.className = `message ${isBot ? "bot" : "user"}`;

        let html = `
            <div class="avatar">
                <span class="material-symbols-outlined"
                      style="font-variation-settings:'FILL' ${isBot ? 1 : 0};">
                    ${isBot ? "precision_manufacturing" : "person"}
                </span>
            </div>
            <div>
                <div class="bubble">${escapeHtml(text)}</div>
        `;

        if (isBot && products && products.length > 0) {
            products.forEach(p => {
                html += `
                <div class="product-highlight">
                    <div class="product-row">
                        <div class="product-img-box">
                            <img src="${p.image}" alt="${escapeHtml(p.name)}" loading="lazy">
                        </div>
                        <div class="product-info">
                            <span class="sku">SKU: ${escapeHtml(p.sku)}</span>
                            <h3 class="product-name">${escapeHtml(p.name)}</h3>
                            <div class="product-price">&#x20B9;${p.price}</div>
                            <div class="badge-row">
                                <span class="badge">${p.stock} IN STOCK</span>
                                <span class="badge">PRO GRADE</span>
                            </div>
                            <div class="btn-group">
                                <button class="btn btn-primary buy-btn"
                                        data-id="${p.id}"
                                        data-name="${escapeHtml(p.name)}"
                                        data-price="${p.price}"
                                        data-image="${p.image}">
                                    Buy Now
                                </button>
                                <button class="btn btn-outline">Full Specs</button>
                            </div>
                        </div>
                    </div>
                </div>`;
            });
        }

        html += `</div>`;
        wrap.innerHTML = html;
        chatBox.appendChild(wrap);
        chatBox.scrollTop = chatBox.scrollHeight;

        // Wire up buy buttons in this new message
        wrap.querySelectorAll(".buy-btn").forEach(btn => {
            btn.addEventListener("click", () => {
                openBuyPanel(
                    btn.dataset.id,
                    btn.dataset.name,
                    btn.dataset.price,
                    btn.dataset.image
                );
            });
        });
    };

    // ----------------------------------------
    // Helper: Show a typing indicator
    // ----------------------------------------
    const showTyping = () => {
        const el = document.createElement("div");
        el.id = "typing-indicator";
        el.className = "message bot";
        el.innerHTML = `
            <div class="avatar">
                <span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1;">
                    precision_manufacturing
                </span>
            </div>
            <div class="bubble" style="display:flex;gap:4px;align-items:center;padding:0.875rem 1.125rem;">
                <span style="width:6px;height:6px;border-radius:50%;background:var(--primary);animation:blink 1s 0.0s infinite;display:inline-block;"></span>
                <span style="width:6px;height:6px;border-radius:50%;background:var(--primary);animation:blink 1s 0.2s infinite;display:inline-block;"></span>
                <span style="width:6px;height:6px;border-radius:50%;background:var(--primary);animation:blink 1s 0.4s infinite;display:inline-block;"></span>
            </div>
        `;
        chatBox.appendChild(el);
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    const hideTyping = () => {
        const el = document.getElementById("typing-indicator");
        if (el) el.remove();
    };

    // ----------------------------------------
    // Send Message
    // ----------------------------------------
    const sendMessage = (query) => {
        query = query.trim();
        if (!query) return;

        addMessage(query, false);
        userInput.value = "";
        sendBtn.disabled = true;
        showTyping();

        fetch('/api/chatbot/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({
                query: query
            })
        })
        .then(res => {
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            return res.json();
        })
        .then(data => {
            hideTyping();
            if (data.response) {
                addMessage(data.response, true, data.products || []);
            }
        })
        .catch(err => {
            hideTyping();
            addMessage("Sorry, something went wrong. Please try again.", true);
            console.error("Chatbot error:", err);
        })
        .finally(() => {
            sendBtn.disabled = false;
            userInput.focus();
        });
    };

    // ----------------------------------------
    // Event Listeners
    // ----------------------------------------
    sendBtn.addEventListener("click", () => sendMessage(userInput.value));

    userInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage(userInput.value);
        }
    });

    document.querySelectorAll(".suggestion").forEach(btn => {
        btn.addEventListener("click", () => sendMessage(btn.textContent.trim()));
    });

    // ----------------------------------------
    // Utility: Escape HTML to prevent XSS
    // ----------------------------------------
    function escapeHtml(str) {
        const div = document.createElement("div");
        div.appendChild(document.createTextNode(String(str)));
        return div.innerHTML;
    }
});

// CSS for blinking dots
const blinkStyle = document.createElement("style");
blinkStyle.textContent = `
@keyframes blink {
    0%, 80%, 100% { opacity: 0.2; transform: scale(0.8); }
    40%            { opacity: 1.0; transform: scale(1.1); }
}`;
document.head.appendChild(blinkStyle);
