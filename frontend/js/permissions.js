/**
 * Permissions and Role Access Control
 */
const permissions = {
  hasRole(role) {
    const current = auth.getRole();
    return current === role;
  },

  hasAnyRole(roles = []) {
    const current = auth.getRole();
    return roles.includes(current);
  },

  canEditAcademicData() {
    return this.hasAnyRole(['ADMIN']);
  },

  canMarkAttendance() {
    return this.hasAnyRole(['ADMIN', 'TEACHER', 'PRINCIPAL']);
  },

  canGradeAssignments() {
    return this.hasAnyRole(['ADMIN', 'TEACHER']);
  },

  canPublishExams() {
    return this.hasAnyRole(['ADMIN', 'TEACHER', 'PRINCIPAL']);
  },

  canManageFees() {
    return this.hasRole('ADMIN');
  },

  enforcePageAccess(allowedRoles = []) {
    return auth.requireAuth(allowedRoles);
  }
};

window.permissions = permissions;
