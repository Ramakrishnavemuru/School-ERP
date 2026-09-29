/**
 * Reusable Components and Layout Renderer
 */
const components = {
  getNavItems(role) {
    const r = (role || '').toUpperCase();
    switch (r) {
      case 'ADMIN':
        return [
          { section: 'Main' },
          { label: 'Dashboard', icon: '📊', url: '/frontend/admin/dashboard.html' },
          { label: 'User Accounts', icon: '👥', url: '/frontend/admin/users.html' },
          { label: 'Students', icon: '🎓', url: '/frontend/admin/students.html' },
          { label: 'Teachers', icon: '👨‍🏫', url: '/frontend/admin/teachers.html' },
          { label: 'Parents', icon: '👨‍👩‍👧', url: '/frontend/admin/parents.html' },
          { section: 'Academic Management' },
          { label: 'Academic Years', icon: '📅', url: '/frontend/admin/academic-years.html' },
          { label: 'Departments', icon: '🏢', url: '/frontend/admin/departments.html' },
          { label: 'Classes', icon: '🏫', url: '/frontend/admin/classes.html' },
          { label: 'Sections', icon: '🚪', url: '/frontend/admin/sections.html' },
          { label: 'Subjects', icon: '📚', url: '/frontend/admin/subjects.html' },
          { label: 'Timetable', icon: '⏰', url: '/frontend/admin/timetable.html' },
          { section: 'Finance & Communications' },
          { label: 'Fees & Payments', icon: '💳', url: '/frontend/admin/fees.html' },
          { label: 'Notices', icon: '📢', url: '/frontend/admin/notices.html' },
          { label: 'Reports', icon: '📈', url: '/frontend/admin/reports.html' },
          { label: 'Audit Logs', icon: '📜', url: '/frontend/admin/audit-logs.html' },
          { label: 'Settings', icon: '⚙️', url: '/frontend/admin/settings.html' }
        ];

      case 'PRINCIPAL':
        return [
          { section: 'Principal Portal' },
          { label: 'Dashboard', icon: '📊', url: '/frontend/principal/dashboard.html' },
          { label: 'Students Directory', icon: '🎓', url: '/frontend/principal/students.html' },
          { label: 'Teachers Directory', icon: '👨‍🏫', url: '/frontend/principal/teachers.html' },
          { label: 'Attendance Overview', icon: '📋', url: '/frontend/principal/attendance.html' },
          { label: 'Academic Performance', icon: '🏆', url: '/frontend/principal/performance.html' },
          { label: 'Leave Requests', icon: '🏖️', url: '/frontend/principal/leave-requests.html' },
          { label: 'Complaints', icon: '⚠️', url: '/frontend/principal/complaints.html' },
          { label: 'School Notices', icon: '📢', url: '/frontend/principal/notices.html' },
          { label: 'Executive Reports', icon: '📈', url: '/frontend/principal/reports.html' }
        ];

      case 'TEACHER':
        return [
          { section: 'Teacher Portal' },
          { label: 'Dashboard', icon: '📊', url: '/frontend/teacher/dashboard.html' },
          { label: 'My Classes', icon: '🏫', url: '/frontend/teacher/my-classes.html' },
          { label: 'My Students', icon: '🎓', url: '/frontend/teacher/students.html' },
          { label: 'Daily Timetable', icon: '⏰', url: '/frontend/teacher/timetable.html' },
          { label: 'Mark Attendance', icon: '📋', url: '/frontend/teacher/attendance.html' },
          { section: 'Academics' },
          { label: 'Assignments', icon: '📝', url: '/frontend/teacher/assignments.html' },
          { label: 'Submissions', icon: '📥', url: '/frontend/teacher/submissions.html' },
          { label: 'Study Materials', icon: '📂', url: '/frontend/teacher/study-materials.html' },
          { label: 'Exams', icon: '📑', url: '/frontend/teacher/exams.html' },
          { label: 'Enter Marks', icon: '✍️', url: '/frontend/teacher/marks.html' },
          { section: 'Personal' },
          { label: 'Leave Applications', icon: '🏖️', url: '/frontend/teacher/leave.html' },
          { label: 'My Profile', icon: '👤', url: '/frontend/teacher/profile.html' }
        ];

      case 'STUDENT':
        return [
          { section: 'Student Portal' },
          { label: 'Dashboard', icon: '📊', url: '/frontend/student/dashboard.html' },
          { label: 'Class Timetable', icon: '⏰', url: '/frontend/student/timetable.html' },
          { label: 'Attendance', icon: '📋', url: '/frontend/student/attendance.html' },
          { label: 'Assignments', icon: '📝', url: '/frontend/student/assignments.html' },
          { label: 'Study Materials', icon: '📂', url: '/frontend/student/study-materials.html' },
          { label: 'Exams', icon: '📑', url: '/frontend/student/exams.html' },
          { label: 'Report Cards', icon: '🏆', url: '/frontend/student/results.html' },
          { label: 'Fees & Dues', icon: '💳', url: '/frontend/student/fees.html' },
          { label: 'Announcements', icon: '📢', url: '/frontend/student/notices.html' },
          { label: 'School Events', icon: '🎉', url: '/frontend/student/events.html' },
          { label: 'Apply Leave', icon: '🏖️', url: '/frontend/student/leave.html' },
          { label: 'Documents', icon: '📄', url: '/frontend/student/documents.html' },
          { label: 'My Profile', icon: '👤', url: '/frontend/student/profile.html' }
        ];

      case 'PARENT':
        return [
          { section: 'Parent Portal' },
          { label: 'Dashboard', icon: '📊', url: '/frontend/parent/dashboard.html' },
          { label: 'My Children', icon: '👨‍👧‍👦', url: '/frontend/parent/children.html' },
          { label: 'Child Attendance', icon: '📋', url: '/frontend/parent/attendance.html' },
          { label: 'Assignments', icon: '📝', url: '/frontend/parent/assignments.html' },
          { label: 'Exam Results', icon: '🏆', url: '/frontend/parent/results.html' },
          { label: 'Fee Payments', icon: '💳', url: '/frontend/parent/fees.html' },
          { label: 'School Notices', icon: '📢', url: '/frontend/parent/notices.html' },
          { label: 'Calendar Events', icon: '🎉', url: '/frontend/parent/events.html' },
          { label: 'Leave Requests', icon: '🏖️', url: '/frontend/parent/leave.html' },
          { label: 'Messages', icon: '✉️', url: '/frontend/parent/messages.html' },
          { label: 'Documents', icon: '📄', url: '/frontend/parent/documents.html' }
        ];

      default:
        return [];
    }
  },

  renderLayout(pageTitle = 'Dashboard') {
    const user = auth.getUser() || { full_name: 'User', role: 'GUEST' };
    const navItems = this.getNavItems(user.role);
    const currentPath = window.location.pathname;

    // Render Sidebar
    let navHtml = '';
    navItems.forEach(item => {
      if (item.section) {
        navHtml += `<div class="nav-section-title">${item.section}</div>`;
      } else {
        const isActive = currentPath === item.url || currentPath.endsWith(item.url.split('/').pop());
        navHtml += `
          <a href="${item.url}" class="sidebar-link ${isActive ? 'active' : ''}">
            <span class="icon">${item.icon}</span>
            <span>${item.label}</span>
          </a>
        `;
      }
    });

    const sidebarContainer = document.getElementById('sidebar-container');
    if (sidebarContainer) {
      sidebarContainer.innerHTML = `
        <div class="sidebar-backdrop" onclick="components.toggleSidebar()"></div>
        <aside class="app-sidebar" id="app-sidebar">
          <div class="sidebar-header">
            <div style="font-size:1.4rem;">🎓</div>
            <div>
              <div class="sidebar-brand">School ERP</div>
              <span class="sidebar-role-badge">${user.role}</span>
            </div>
          </div>
          <nav class="sidebar-nav">
            ${navHtml}
          </nav>
        </aside>
      `;
    }

    // Render Navbar
    const navbarContainer = document.getElementById('navbar-container');
    if (navbarContainer) {
      navbarContainer.innerHTML = `
        <header class="app-navbar">
          <div class="d-flex align-items-center gap-3">
            <button class="btn btn-sm btn-outline-secondary sidebar-toggle-btn" onclick="components.toggleSidebar()">
              ☰
            </button>
            <h5 class="m-0 fw-bold d-none d-sm-block text-dark">${pageTitle}</h5>
          </div>

          <div class="d-flex align-items-center gap-3">
            <!-- Notifications Bell -->
            <div class="dropdown">
              <button class="btn btn-light position-relative p-2" type="button" id="notifDropdown" data-bs-toggle="dropdown" aria-expanded="false" onclick="components.loadNotifications()">
                🔔
                <span id="notif-badge" class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger d-none" style="font-size:0.65rem;">
                  0
                </span>
              </button>
              <ul class="dropdown-menu dropdown-menu-end shadow border-0 p-2" aria-labelledby="notifDropdown" style="width: 320px; max-height: 400px; overflow-y: auto;" id="notif-menu">
                <li class="dropdown-header fw-bold">Notifications</li>
                <li id="notif-empty" class="text-muted small text-center py-3">No notifications</li>
              </ul>
            </div>

            <!-- User Menu -->
            <div class="dropdown">
              <button class="navbar-user-btn" type="button" id="userMenuBtn" data-bs-toggle="dropdown" aria-expanded="false">
                <div class="user-avatar-placeholder">
                  ${user.full_name ? user.full_name.charAt(0).toUpperCase() : 'U'}
                </div>
                <div class="text-start d-none d-md-block">
                  <div style="font-size: 0.85rem; font-weight: 600; line-height: 1.2;">${user.full_name}</div>
                  <div style="font-size: 0.7rem; color: var(--text-muted);">${user.role}</div>
                </div>
              </button>
              <ul class="dropdown-menu dropdown-menu-end shadow border-0" aria-labelledby="userMenuBtn">
                <li><h6 class="dropdown-header">${user.email || user.username}</h6></li>
                <li><hr class="dropdown-divider"></li>
                <li>
                  <a class="dropdown-item text-danger fw-semibold" href="javascript:void(0)" onclick="auth.logout()">
                    🚪 Log Out
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </header>
      `;
    }

    // Load notification count initially
    this.checkUnreadNotifications();
  },

  toggleSidebar() {
    const sidebar = document.getElementById('app-sidebar');
    const backdrop = document.querySelector('.sidebar-backdrop');
    if (sidebar) sidebar.classList.toggle('show');
    if (backdrop) backdrop.classList.toggle('show');
  },

  async checkUnreadNotifications() {
    try {
      if (!auth.isAuthenticated()) return;
      const notifs = await api.get('/notifications', { unread_only: true });
      const badge = document.getElementById('notif-badge');
      if (badge && Array.isArray(notifs)) {
        if (notifs.length > 0) {
          badge.textContent = notifs.length > 9 ? '9+' : notifs.length;
          badge.classList.remove('d-none');
        } else {
          badge.classList.add('d-none');
        }
      }
    } catch (e) {
      // Ignore background check failure
    }
  },

  async loadNotifications() {
    const menu = document.getElementById('notif-menu');
    if (!menu) return;
    try {
      const notifs = await api.get('/notifications');
      if (!notifs || notifs.length === 0) {
        menu.innerHTML = '<li class="dropdown-header fw-bold">Notifications</li><li class="text-muted small text-center py-3">No notifications</li>';
        return;
      }

      let html = `
        <li class="dropdown-header d-flex justify-content-between align-items-center">
          <span class="fw-bold">Notifications</span>
          <button class="btn btn-link btn-sm text-decoration-none p-0" style="font-size:0.75rem;" onclick="components.markAllNotificationsRead(event)">Mark all read</button>
        </li>
        <li><hr class="dropdown-divider my-1"></li>
      `;

      notifs.slice(0, 8).forEach(n => {
        html += `
          <li class="p-2 border-bottom ${n.is_read ? 'bg-white' : 'bg-light'}" style="font-size:0.8rem; cursor:pointer;" onclick="components.readNotification(${n.id})">
            <div class="fw-semibold text-dark">${n.title}</div>
            <div class="text-secondary small text-truncate">${n.message}</div>
            <div class="text-muted" style="font-size:0.7rem;">${utils.formatDate(n.created_at)}</div>
          </li>
        `;
      });
      menu.innerHTML = html;
    } catch (e) {
      menu.innerHTML = '<li class="dropdown-header fw-bold">Notifications</li><li class="text-danger small text-center py-2">Failed to load</li>';
    }
  },

  async markAllNotificationsRead(event) {
    if (event) event.stopPropagation();
    try {
      await api.post('/notifications/read-all', {});
      const badge = document.getElementById('notif-badge');
      if (badge) badge.classList.add('d-none');
      this.loadNotifications();
    } catch (e) {
      utils.showToast('Could not mark all as read', 'danger');
    }
  },

  async readNotification(id) {
    try {
      await api.patch(`/notifications/${id}/read`);
      this.checkUnreadNotifications();
      this.loadNotifications();
    } catch (e) {}
  },

  renderPagination(containerId, currentPage, totalPages, onPageClickFnName) {
    const container = document.getElementById(containerId);
    if (!container) return;
    if (totalPages <= 1) {
      container.innerHTML = '';
      return;
    }

    let html = `<ul class="pagination pagination-sm justify-content-end mb-0">`;
    html += `
      <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
        <a class="page-link" href="javascript:void(0)" onclick="${onPageClickFnName}(${currentPage - 1})">Previous</a>
      </li>
    `;

    for (let p = 1; p <= totalPages; p++) {
      if (p === 1 || p === totalPages || (p >= currentPage - 2 && p <= currentPage + 2)) {
        html += `
          <li class="page-item ${p === currentPage ? 'active' : ''}">
            <a class="page-link" href="javascript:void(0)" onclick="${onPageClickFnName}(${p})">${p}</a>
          </li>
        `;
      } else if (p === currentPage - 3 || p === currentPage + 3) {
        html += `<li class="page-item disabled"><span class="page-link">...</span></li>`;
      }
    }

    html += `
      <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
        <a class="page-link" href="javascript:void(0)" onclick="${onPageClickFnName}(${currentPage + 1})">Next</a>
      </li>
    `;
    html += `</ul>`;
    container.innerHTML = html;
  }
};

window.components = components;
