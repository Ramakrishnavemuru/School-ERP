/**
 * Exams Controller
 */
const examsManager = {
  async init() {
    await this.loadExams();
  },

  async loadExams() {
    const tbody = document.getElementById('exams-table-body');
    if (!tbody) return;

    try {
      const exams = await api.get('/exams');
      if (exams.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="table-empty-state">No exams scheduled.</td></tr>';
        return;
      }

      tbody.innerHTML = exams.map(e => `
        <tr>
          <td><strong>${e.name}</strong></td>
          <td><span class="badge bg-secondary">${e.exam_type}</span></td>
          <td>${e.class_name || 'All Classes'}</td>
          <td>${utils.formatDate(e.start_date)} - ${utils.formatDate(e.end_date)}</td>
          <td>${e.is_published ? '<span class="badge bg-success">Published</span>' : '<span class="badge bg-warning text-dark">Draft</span>'}</td>
          <td>
            <div class="table-actions">
              ${!e.is_published ? `<button class="btn btn-sm btn-outline-success" onclick="examsManager.publishExam(${e.id})">📢 Publish Results</button>` : ''}
              <button class="table-action-btn text-danger" onclick="examsManager.deleteExam(${e.id})">🗑️</button>
            </div>
          </td>
        </tr>
      `).join('');
    } catch (e) {
      tbody.innerHTML = `<tr><td colspan="7" class="text-danger text-center py-3">${e.message}</td></tr>`;
    }
  },

  async createExam(formEvent) {
    if (formEvent) formEvent.preventDefault();
    const form = document.getElementById('create-exam-form');
    if (!form) return;

    const payload = {
      name: form.name.value.trim(),
      exam_type: form.exam_type.value,
      class_id: parseInt(form.class_id.value) || null,
      start_date: form.start_date.value,
      end_date: form.end_date.value,
      is_published: false
    };

    try {
      await api.post('/exams', payload);
      utils.showToast('Exam scheduled successfully!', 'success');
      form.reset();
      const modalEl = document.getElementById('createExamModal');
      if (modalEl && window.bootstrap) {
        const modal = bootstrap.Modal.getInstance(modalEl);
        if (modal) modal.hide();
      }
      this.loadExams();
    } catch (e) {
      utils.showToast(e.message || 'Failed to create exam', 'danger');
    }
  },

  async publishExam(id) {
    if (!confirm('Are you sure you want to publish the results of this exam? Students and parents will be notified.')) return;
    try {
      await api.patch(`/exams/${id}/publish`);
      utils.showToast('Exam results officially published!', 'success');
      this.loadExams();
    } catch (e) {
      utils.showToast(e.message, 'danger');
    }
  },

  async deleteExam(id) {
    if (!confirm('Are you sure you want to delete this exam?')) return;
    try {
      await api.delete(`/exams/${id}`);
      utils.showToast('Exam deleted', 'success');
      this.loadExams();
    } catch (e) {
      utils.showToast(e.message, 'danger');
    }
  }
};

window.examsManager = examsManager;
