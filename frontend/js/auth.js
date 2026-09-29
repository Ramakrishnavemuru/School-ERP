/**
 * Authentication and Session Management
 */
const auth = {
  getUser() {
    try {
      const u = localStorage.getItem('user');
      return u ? JSON.parse(u) : null;
    } catch {
      return null;
    }
  },

  getToken() {
    return localStorage.getItem('token');
  },

  isAuthenticated() {
    return !!this.getToken() && !!this.getUser();
  },

  getRole() {
    const user = this.getUser();
    return user ? user.role : null;
  },

  async login(username, password) {
    const data = await api.post('/auth/login', { username, password });
    localStorage.setItem('token', data.access_token);
    localStorage.setItem('user', JSON.stringify(data.user));
    return data.user;
  },

  async logout() {
    try {
      if (this.isAuthenticated()) {
        await api.post('/auth/logout', {});
      }
    } catch (e) {
      // Ignore network failure on logout
    } finally {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/frontend/login.html';
    }
  },

  getRoleDashboardUrl(role) {
    switch ((role || '').toUpperCase()) {
      case 'ADMIN':
        return '/frontend/admin/dashboard.html';
      case 'PRINCIPAL':
        return '/frontend/principal/dashboard.html';
      case 'TEACHER':
        return '/frontend/teacher/dashboard.html';
      case 'STUDENT':
        return '/frontend/student/dashboard.html';
      case 'PARENT':
        return '/frontend/parent/dashboard.html';
      default:
        return '/frontend/login.html';
    }
  },

  redirectBasedOnRole(role) {
    window.location.href = this.getRoleDashboardUrl(role);
  },

  requireAuth(allowedRoles = []) {
    if (!this.isAuthenticated()) {
      window.location.href = `/frontend/login.html?redirect=${encodeURIComponent(window.location.pathname)}`;
      return false;
    }

    const currentRole = this.getRole();
    if (allowedRoles.length > 0 && !allowedRoles.includes(currentRole)) {
      alert(`Access denied: requires one of [${allowedRoles.join(', ')}]. You are logged in as ${currentRole}.`);
      this.redirectBasedOnRole(currentRole);
      return false;
    }

    return true;
  }
};

window.auth = auth;
