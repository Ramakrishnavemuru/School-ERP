/**
 * Teacher Management Controller
 */
const teachersManager = {
  currentPage: 1,
  pageSize: 10,
  searchTerm: '',
  selectedDept: '',

  async init() {
    await this.loadDepartmentFilters();
    await this.loadTeachers(1);
    this.setupListeners();
  },

  setupListeners() {
    const searchInput = document.getElementById('teacher-search');
    if (searchInput) {
      searchInput.addEventListener('input', utils.debounce((e) => {
        this.searchTerm = e.target.value.trim();
        this.loadTeachers(1);
      }, 350));
    }

    const deptFilter = document.getElementById('filter-dept');
    if (deptFilter) {
      deptFilter.addEventListener('change', (e) => {
        this.selectedDept = e.target.value;
        this.loadTeachers(1);
      });
    }
  },

  async loadDepartmentFilters() {
    const filterSelect = document.getElementById('filter-dept');
    const modalSelect = document.getElementById('modal-teacher-dept');
    try {
      const depts = await api.get('/departments');
      let optionsHtml = '<option value="">All Departments</option>';
      let modalOptionsHtml = '<option value="">Select Department</option>';

      depts.forEach(d => {
        optionsHtml += `<option value="${d.id}">${d.name}</option>`;
        modalOptionsHtml += `<option value="${d.id}">${d.name}</option>`;
      });

      if (filterSelect) filterSelect.innerHTML = optionsHtml;
      if (modalSelect) modalSelect.innerHTML = modalOptionsHtml;
    } catch (e) {
      console.error('Failed to load department filters', e);
    }
  },

  async loadTeachers(page = 1) {
    this.currentPage = page;
    const tbody = document.getElementById('teachers-table-body');
    if (tbody) tbody.innerHTML = '<tr><td colspan="7" class="text-center py-4 text-muted">Loading teachers...</td></tr>';

    try {
      const res = await api.get('/teachers', {
        page: this.currentPage,
        page_size: this.pageSize,
        search: this.searchTerm,
        department_id: this.selectedDept
      });

      if (!tbody) return;

      if (!res.items || res.items.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="table-empty-state">No teachers found.</td></tr>';
        components.renderPagination('pagination-container', 1, 1, 'teachersManager.loadTeachers');
        return;
      }

      tbody.innerHTML = res.items.map(t => `
        <tr>
          <td><strong>${t.employee_id}</strong></td>
          <td>
            <div class="fw-bold">${t.user ? t.user.full_name : '—'}</div>
            <div class="text-muted small">${t.user ? t.user.email : ''}</div>
          </td>
          <td>${t.department_name || 'General'}</td>
          <td>${t.designation || 'Teacher'}</td>
          <td>${t.qualification || '—'}</td>
          <td>${t.phone || (t.user ? t.user.phone : '—')}</td>
          <td>
            <div class="table-actions">
              <a href="/frontend/admin/teacher-details.html?id=${t.id}" class="table-action-btn" title="View Details">👁️ View</a>
              <button class="table-action-btn text-danger" onclick="teachersManager.deleteTeacher(${t.id})" title="Delete">🗑️</button>
            </div>
          </td>
        </tr>
      `).join('');

      components.renderPagination('pagination-container', res.page, res.total_pages, 'teachersManager.loadTeachers');
    } catch (e) {
      if (tbody) tbody.innerHTML = `<tr><td colspan="7" class="text-center py-4 text-danger">${e.message || 'Error loading teachers'}</td></tr>`;
    }
  },

  async createTeacher(formEvent) {
    if (formEvent) formEvent.preventDefault();
    const form = document.getElementById('add-teacher-form');
    if (!form) return;

    const payload = {
      username: form.username.value.trim(),
      email: form.email.value.trim(),
      password: form.password.value,
      full_name: form.full_name.value.trim(),
      phone: form.phone.value.trim(),
      employee_id: form.employee_id.value.trim(),
      department_id: parseInt(form.department_id.value) || null,
      designation: form.designation.value.trim() || 'Teacher',
      qualification: form.qualification.value.trim() || null,
      address: form.address.value.trim() || null
    };

    try {
      await api.post('/teachers', payload);
      utils.showToast('Teacher registered successfully!', 'success');
      const modalEl = document.getElementById('addTeacherModal');
      if (modalEl && window.bootstrap) {
        const modal = bootstrap.Modal.getInstance(modalEl);
        if (modal) modal.hide();
      }
      form.reset();
      this.loadTeachers(1);
    } catch (e) {
      utils.showToast(e.message || 'Failed to create teacher', 'danger');
    }
  },

  async deleteTeacher(id) {
    if (!confirm('Are you sure you want to delete this teacher account?')) return;
    try {
      await api.delete(`/teachers/${id}`);
      utils.showToast('Teacher deleted successfully', 'success');
      this.loadTeachers(this.currentPage);
    } catch (e) {
      utils.showToast(e.message || 'Failed to delete teacher', 'danger');
    }
  },

  async loadTeacherDetails() {
    const params = utils.getQueryParams();
    const id = params.id;
    if (!id) return;

    try {
      const teacher = await api.get(`/teachers/${id}`);
      const setText = (id, val) => {
        const el = document.getElementById(id);
        if (el) el.textContent = val || '—';
      };

      setText('detail-name', teacher.user ? teacher.user.full_name : '');
      setText('detail-empid', teacher.employee_id);
      setText('detail-dept', teacher.department_name);
      setText('detail-designation', teacher.designation);
      setText('detail-email', teacher.user ? teacher.user.email : '');
      setText('detail-phone', teacher.phone || (teacher.user ? teacher.user.phone : ''));
      setText('detail-qual', teacher.qualification);
      setText('detail-address', teacher.address);

      // Subjects taught
      const subjectsList = document.getElementById('teacher-subjects-list');
      if (subjectsList && teacher.subjects) {
        subjectsList.innerHTML = teacher.subjects.map(s => `
          <li class="list-group-item d-flex justify-content-between align-items-center">
            <span><strong>${s.name}</strong> (${s.code})</span>
            <span class="badge bg-secondary">${s.class_name}</span>
          </li>
        `).join('') || '<li class="list-group-item text-muted">No assigned subjects</li>';
      }
    } catch (e) {
      utils.showToast(e.message || 'Failed to load teacher details', 'danger');
    }
  }
};

window.teachersManager = teachersManager;
