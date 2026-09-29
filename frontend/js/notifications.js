/**
 * Notifications Controller
 */
const notificationsManager = {
  async init() {
    await this.loadAllNotifications();
  },

  async loadAllNotifications() {
    const listEl = document.getElementById('notifications-full-list');
    if (!listEl) return;

    try {
      const notifs = await api.get('/notifications');
      if (notifs.length === 0) {
        listEl.innerHTML = '<div class="text-center py-5 text-muted">No notifications in your inbox.</div>';
        return;
      }

      listEl.innerHTML = notifs.map(n => `
        <div class="card card-custom mb-2 p-3 ${n.is_read ? '' : 'border-primary'}" style="${n.is_read ? '' : 'background-color:#f8fafc;'}">
          <div class="d-flex justify-content-between align-items-center mb-1">
            <h6 class="fw-bold mb-0 text-dark">${n.title}</h6>
            <span class="text-muted small">${utils.formatDateTime(n.created_at)}</span>
          </div>
          <p class="text-secondary small mb-2">${n.message}</p>
          <div class="d-flex justify-content-between align-items-center">
            <span class="badge bg-secondary">${n.notification_type}</span>
            ${!n.is_read ? `<button class="btn btn-sm btn-link text-decoration-none p-0" onclick="notificationsManager.markRead(${n.id})">Mark as read</button>` : '<span class="text-muted small">Read</span>'}
          </div>
        </div>
      `).join('');
    } catch (e) {
      listEl.innerHTML = `<div class="text-danger py-4 text-center">${e.message}</div>`;
    }
  },

  async markRead(id) {
    try {
      await api.patch(`/notifications/${id}/read`);
      this.loadAllNotifications();
      components.checkUnreadNotifications();
    } catch (e) {
      utils.showToast(e.message, 'danger');
    }
  }
};

window.notificationsManager = notificationsManager;
