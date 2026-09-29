/**
 * Attendance Management Controller
 */
const attendanceManager = {
  currentStudents: [],

  async initTeacher() {
    await this.loadClassSelect();
    const today = new Date().toISOString().split('T')[0];
    const dateInput = document.getElementById('attendance-date');
    if (dateInput) dateInput.value = today;
  },

  async loadClassSelect() {
    const classSelect = document.getElementById('att-class-select');
    const secSelect = document.getElementById('att-section-select');
    if (!classSelect) return;

    try {
      const classes = await api.get('/classes');
      classSelect.innerHTML = '<option value="">Select Class</option>' +
        classes.map(c => `<option value="${c.id}">${c.name}</option>`).join('');

      classSelect.addEventListener('change', () => {
        const selectedId = parseInt(classSelect.value);
        const selClass = classes.find(c => c.id === selectedId);
        if (secSelect && selClass) {
          secSelect.innerHTML = '<option value="">Select Section</option>' +
            selClass.sections.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
        }
      });
    } catch (e) {
      console.error(e);
    }
  },

  async loadClassStudents() {
    const classId = document.getElementById('att-class-select').value;
    const sectionId = document.getElementById('att-section-select').value;
    const attDate = document.getElementById('attendance-date').value;

    if (!classId) {
      utils.showToast('Please select a class', 'warning');
      return;
    }

    const tbody = document.getElementById('attendance-marking-tbody');
    if (tbody) tbody.innerHTML = '<tr><td colspan="5" class="text-center py-4 text-muted">Loading students...</td></tr>';

    try {
      // Fetch students for this class and section
      const res = await api.get('/students', { class_id: classId, section_id: sectionId, page_size: 100 });
      this.currentStudents = res.items || [];

      // Fetch any existing attendance for this class and date
      const existing = await api.get('/attendance', { class_id: classId, section_id: sectionId, att_date: attDate });
      const attMap = {};
      if (Array.isArray(existing)) {
        existing.forEach(a => { attMap[a.student_id] = a.status; });
      }

      if (this.currentStudents.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="table-empty-state">No students found in this class.</td></tr>';
        return;
      }

      tbody.innerHTML = this.currentStudents.map((s, idx) => {
        const currentStatus = attMap[s.id] || 'Present';
        return `
          <tr>
            <td>${idx + 1}</td>
            <td><strong>${s.admission_number}</strong></td>
            <td>${s.user ? s.user.full_name : ''}</td>
            <td>${s.roll_number || '—'}</td>
            <td>
              <div class="btn-group btn-group-sm" role="group">
                <input type="radio" class="btn-check" name="status_${s.id}" id="p_${s.id}" value="Present" ${currentStatus === 'Present' ? 'checked' : ''}>
                <label class="btn btn-outline-success" for="p_${s.id}">Present</label>

                <input type="radio" class="btn-check" name="status_${s.id}" id="l_${s.id}" value="Late" ${currentStatus === 'Late' ? 'checked' : ''}>
                <label class="btn btn-outline-warning" for="l_${s.id}">Late</label>

                <input type="radio" class="btn-check" name="status_${s.id}" id="a_${s.id}" value="Absent" ${currentStatus === 'Absent' ? 'checked' : ''}>
                <label class="btn btn-outline-danger" for="a_${s.id}">Absent</label>
              </div>
            </td>
          </tr>
        `;
      }).join('');

      const submitBtn = document.getElementById('save-attendance-btn');
      if (submitBtn) submitBtn.classList.remove('d-none');
    } catch (e) {
      if (tbody) tbody.innerHTML = `<tr><td colspan="5" class="text-center py-4 text-danger">${e.message || 'Error'}</td></tr>`;
    }
  },

  async saveAttendance() {
    const classId = document.getElementById('att-class-select').value;
    const sectionId = document.getElementById('att-section-select').value;
    const attDate = document.getElementById('attendance-date').value;

    if (!classId || !attDate) {
      utils.showToast('Please select class and date', 'warning');
      return;
    }

    const records = [];
    this.currentStudents.forEach(s => {
      const selected = document.querySelector(`input[name="status_${s.id}"]:checked`);
      records.push({
        student_id: s.id,
        status: selected ? selected.value : 'Present',
        remarks: null
      });
    });

    try {
      await api.post('/attendance', {
        class_id: parseInt(classId),
        section_id: parseInt(sectionId) || 1,
        date: attDate,
        records: records
      });
      utils.showToast('Attendance recorded successfully!', 'success');
    } catch (e) {
      utils.showToast(e.message || 'Failed to save attendance', 'danger');
    }
  },

  async loadStudentAttendanceHistory() {
    const tbody = document.getElementById('student-attendance-tbody');
    try {
      const data = await api.get('/student/attendance');
      if (data && data.stats) {
        const setText = (id, val) => {
          const el = document.getElementById(id);
          if (el) el.textContent = val;
        };
        setText('att-pct', `${data.stats.percentage}%`);
        setText('att-total-days', data.stats.total_days);
        setText('att-present-days', data.stats.present_days);
        setText('att-absent-days', data.stats.absent_days);
        setText('att-late-days', data.stats.late_days);
      }

      if (tbody && data.records) {
        if (data.records.length === 0) {
          tbody.innerHTML = '<tr><td colspan="3" class="table-empty-state">No attendance records found.</td></tr>';
          return;
        }
        tbody.innerHTML = data.records.map(r => `
          <tr>
            <td>${utils.formatDate(r.date)}</td>
            <td>${utils.getStatusBadge(r.status)}</td>
            <td>${r.remarks || '—'}</td>
          </tr>
        `).join('');
      }
    } catch (e) {
      if (tbody) tbody.innerHTML = `<tr><td colspan="3" class="text-danger py-3 text-center">${e.message}</td></tr>`;
    }
  }
};

window.attendanceManager = attendanceManager;
