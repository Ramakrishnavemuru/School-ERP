/**
 * Student Management Controller
 */
const studentsManager = {
  currentPage: 1,
  pageSize: 10,
  searchTerm: '',
  selectedClass: '',
  selectedSection: '',

  async init() {
    await this.loadClassFilters();
    await this.loadStudents(1);
    this.setupListeners();
  },

  setupListeners() {
    const searchInput = document.getElementById('student-search');
    if (searchInput) {
      searchInput.addEventListener('input', utils.debounce((e) => {
        this.searchTerm = e.target.value.trim();
        this.loadStudents(1);
      }, 350));
    }

    const classFilter = document.getElementById('filter-class');
    if (classFilter) {
      classFilter.addEventListener('change', (e) => {
        this.selectedClass = e.target.value;
        this.loadStudents(1);
      });
    }
  },

  async loadClassFilters() {
    const filterSelect = document.getElementById('filter-class');
    const modalSelect = document.getElementById('modal-student-class');
    try {
      const classes = await api.get('/classes');
      let optionsHtml = '<option value="">All Classes</option>';
      let modalOptionsHtml = '<option value="">Select Class</option>';

      classes.forEach(c => {
        optionsHtml += `<option value="${c.id}">${c.name}</option>`;
        modalOptionsHtml += `<option value="${c.id}">${c.name}</option>`;
      });

      if (filterSelect) filterSelect.innerHTML = optionsHtml;
      if (modalSelect) modalSelect.innerHTML = modalOptionsHtml;
    } catch (e) {
      console.error('Failed to load class filters', e);
    }
  },

  async loadStudents(page = 1) {
    this.currentPage = page;
    const tbody = document.getElementById('students-table-body');
    if (tbody) tbody.innerHTML = '<tr><td colspan="7" class="text-center py-4 text-muted">Loading students...</td></tr>';

    try {
      const res = await api.get('/students', {
        page: this.currentPage,
        page_size: this.pageSize,
        search: this.searchTerm,
        class_id: this.selectedClass
      });

      if (!tbody) return;

      if (!res.items || res.items.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="table-empty-state">No students found matching criteria.</td></tr>';
        components.renderPagination('pagination-container', 1, 1, 'studentsManager.loadStudents');
        return;
      }

      tbody.innerHTML = res.items.map(s => `
        <tr>
          <td><strong>${s.admission_number}</strong></td>
          <td>
            <div class="fw-bold">${s.user ? s.user.full_name : '—'}</div>
            <div class="text-muted small">${s.user ? s.user.email : ''}</div>
          </td>
          <td>${s.class_name || '—'} ${s.section_name ? `(${s.section_name})` : ''}</td>
          <td>${s.roll_number || '—'}</td>
          <td>${s.gender || '—'}</td>
          <td>${s.parent_name || '—'}</td>
          <td>
            <div class="table-actions">
              <a href="/frontend/admin/student-details.html?id=${s.id}" class="table-action-btn" title="View Details">👁️ View</a>
              <button class="table-action-btn text-danger" onclick="studentsManager.deleteStudent(${s.id})" title="Delete">🗑️</button>
            </div>
          </td>
        </tr>
      `).join('');

      components.renderPagination('pagination-container', res.page, res.total_pages, 'studentsManager.loadStudents');
    } catch (e) {
      if (tbody) tbody.innerHTML = `<tr><td colspan="7" class="text-center py-4 text-danger">${e.message || 'Error loading students'}</td></tr>`;
    }
  },

  async createStudent(formEvent) {
    if (formEvent) formEvent.preventDefault();
    const form = document.getElementById('add-student-form');
    if (!form) return;

    const payload = {
      username: form.username.value.trim(),
      email: form.email.value.trim(),
      password: form.password.value,
      full_name: form.full_name.value.trim(),
      phone: form.phone.value.trim(),
      admission_number: form.admission_number.value.trim(),
      roll_number: form.roll_number.value.trim() || null,
      class_id: parseInt(form.class_id.value) || null,
      gender: form.gender.value || null,
      date_of_birth: form.date_of_birth.value || null,
      address: form.address.value.trim() || null
    };

    try {
      await api.post('/students', payload);
      utils.showToast('Student registered successfully!', 'success');
      const modalEl = document.getElementById('addStudentModal');
      if (modalEl && window.bootstrap) {
        const modal = bootstrap.Modal.getInstance(modalEl);
        if (modal) modal.hide();
      }
      form.reset();
      this.loadStudents(1);
    } catch (e) {
      utils.showToast(e.message || 'Failed to create student', 'danger');
    }
  },

  async deleteStudent(id) {
    if (!confirm('Are you sure you want to permanently delete this student record?')) return;
    try {
      await api.delete(`/students/${id}`);
      utils.showToast('Student deleted successfully', 'success');
      this.loadStudents(this.currentPage);
    } catch (e) {
      utils.showToast(e.message || 'Failed to delete student', 'danger');
    }
  },

  async loadStudentDetails() {
    const params = utils.getQueryParams();
    const id = params.id;
    if (!id) return;

    try {
      const student = await api.get(`/students/${id}`);
      const setText = (id, val) => {
        const el = document.getElementById(id);
        if (el) el.textContent = val || '—';
      };

      setText('detail-name', student.user ? student.user.full_name : '');
      setText('detail-adm', student.admission_number);
      setText('detail-roll', student.roll_number);
      setText('detail-class', `${student.class_name || ''} ${student.section_name ? `(${student.section_name})` : ''}`);
      setText('detail-email', student.user ? student.user.email : '');
      setText('detail-phone', student.user ? student.user.phone : '');
      setText('detail-gender', student.gender);
      setText('detail-blood', student.blood_group);
      setText('detail-dob', utils.formatDate(student.date_of_birth));
      setText('detail-parent', student.parent_name);
      setText('detail-address', student.address);

      // Load attendance & fees
      const att = await api.get(`/students/${id}/attendance`);
      if (att && att.stats) {
        setText('att-percentage', `${att.stats.percentage}%`);
        setText('att-present', `${att.stats.present_days} / ${att.stats.total_days} Days`);
      }

      const fees = await api.get(`/students/${id}/fees`);
      if (fees) {
        setText('fee-total', utils.formatCurrency(fees.total_fees));
        setText('fee-paid', utils.formatCurrency(fees.total_paid));
        setText('fee-balance', utils.formatCurrency(fees.remaining_balance));
      }
    } catch (e) {
      utils.showToast(e.message || 'Failed to load student details', 'danger');
    }
  }
};

window.studentsManager = studentsManager;
