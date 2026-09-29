/**
 * Messaging Controller
 */
const messagesManager = {
  currentTab: 'inbox',

  async init() {
    await this.loadMessages('inbox');
    await this.loadUsersForCompose();
  },

  async loadUsersForCompose() {
    const sel = document.getElementById('compose-recipient');
    if (!sel) return;
    try {
      const res = await api.get('/users', { page_size: 100 });
      if (res && res.items) {
        sel.innerHTML = '<option value="">Select Recipient</option>' +
          res.items.map(u => `<option value="${u.id}">${u.full_name} (${u.role})</option>`).join('');
      }
    } catch (e) {
      console.error(e);
    }
  },

  async loadMessages(tab = 'inbox') {
    this.currentTab = tab;
    const container = document.getElementById('messages-list-container');
    if (!container) return;

    try {
      const msgs = await api.get(`/messages/${tab}`);
      if (msgs.length === 0) {
        container.innerHTML = `<div class="text-center py-5 text-muted">No ${tab} messages.</div>`;
        return;
      }

      container.innerHTML = msgs.map(m => `
        <div class="card card-custom mb-3 p-3 ${!m.is_read && tab === 'inbox' ? 'border-primary' : ''}">
          <div class="d-flex justify-content-between align-items-center mb-1">
            <h6 class="fw-bold mb-0 text-dark">${m.subject}</h6>
            <span class="text-muted small">${utils.formatDateTime(m.sent_at)}</span>
          </div>
          <div class="text-muted small mb-2">
            ${tab === 'inbox' ? `From: <strong>${m.sender_name}</strong> (${m.sender_role})` : `To: <strong>${m.receiver_name}</strong>`}
          </div>
          <p class="text-secondary small mb-2" style="white-space: pre-wrap;">${m.body}</p>
          ${tab === 'inbox' && !m.is_read ? `
            <div class="text-end">
              <button class="btn btn-sm btn-outline-secondary" onclick="messagesManager.markAsRead(${m.id})">Mark as read</button>
            </div>
          ` : ''}
        </div>
      `).join('');
    } catch (e) {
      container.innerHTML = `<div class="text-danger py-4 text-center">${e.message}</div>`;
    }
  },

  async sendMessage(formEvent) {
    if (formEvent) formEvent.preventDefault();
    const form = document.getElementById('compose-message-form');
    if (!form) return;

    const payload = {
      receiver_id: parseInt(form.receiver_id.value),
      subject: form.subject.value.trim(),
      body: form.body.value.trim()
    };

    try {
      await api.post('/messages', payload);
      utils.showToast('Message sent successfully!', 'success');
      form.reset();
      const modalEl = document.getElementById('composeModal');
      if (modalEl && window.bootstrap) {
        const modal = bootstrap.Modal.getInstance(modalEl);
        if (modal) modal.hide();
      }
      if (this.currentTab === 'sent') {
        this.loadMessages('sent');
      }
    } catch (e) {
      utils.showToast(e.message || 'Failed to send message', 'danger');
    }
  },

  async markAsRead(id) {
    try {
      await api.patch(`/messages/${id}/read`);
      this.loadMessages(this.currentTab);
    } catch (e) {
      utils.showToast(e.message, 'danger');
    }
  }
};

window.messagesManager = messagesManager;
