/**
 * Results and Marks Controller
 */
const resultsManager = {
  currentStudents: [],

  async initMarksEntry() {
    await this.loadFilters();
  },

  async loadFilters() {
    const examSelect = document.getElementById('marks-exam');
    const classSelect = document.getElementById('marks-class');
    const subjSelect = document.getElementById('marks-subject');

    try {
      const exams = await api.get('/exams');
      if (examSelect) {
        examSelect.innerHTML = '<option value="">Select Exam</option>' +
          exams.map(e => `<option value="${e.id}">${e.name} (${e.exam_type})</option>`).join('');
      }

      const classes = await api.get('/classes');
      if (classSelect) {
        classSelect.innerHTML = '<option value="">Select Class</option>' +
          classes.map(c => `<option value="${c.id}">${c.name}</option>`).join('');
      }

      const subjects = await api.get('/subjects');
      if (subjSelect) {
        subjSelect.innerHTML = '<option value="">Select Subject</option>' +
          subjects.map(s => `<option value="${s.id}">${s.name} (${s.code})</option>`).join('');
      }
    } catch (e) {
      console.error(e);
    }
  },

  async loadStudentsForMarks() {
    const examId = document.getElementById('marks-exam').value;
    const classId = document.getElementById('marks-class').value;
    const subjectId = document.getElementById('marks-subject').value;

    if (!examId || !classId || !subjectId) {
      utils.showToast('Please select Exam, Class, and Subject', 'warning');
      return;
    }

    const tbody = document.getElementById('marks-entry-tbody');
    if (tbody) tbody.innerHTML = '<tr><td colspan="5" class="text-center py-4 text-muted">Loading students...</td></tr>';

    try {
      const res = await api.get('/students', { class_id: classId, page_size: 100 });
      this.currentStudents = res.items || [];

      // Fetch existing results
      const existingResults = await api.get('/results', { exam_id: examId, subject_id: subjectId });
      const marksMap = {};
      if (Array.isArray(existingResults)) {
        existingResults.forEach(r => { marksMap[r.student_id] = r; });
      }

      if (this.currentStudents.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="table-empty-state">No students found in this class.</td></tr>';
        return;
      }

      tbody.innerHTML = this.currentStudents.map((s, idx) => {
        const existing = marksMap[s.id];
        return `
          <tr>
            <td>${idx + 1}</td>
            <td><strong>${s.admission_number}</strong></td>
            <td>${s.user ? s.user.full_name : ''}</td>
            <td>
              <input type="number" step="0.5" min="0" max="100" class="form-control form-control-sm marks-input"
                id="marks_${s.id}" value="${existing ? existing.marks_obtained : ''}" placeholder="0 - 100" style="width:120px;" required>
            </td>
            <td>
              <input type="text" class="form-control form-control-sm remarks-input"
                id="remarks_${s.id}" value="${existing && existing.remarks ? existing.remarks : ''}" placeholder="Remarks (optional)">
            </td>
          </tr>
        `;
      }).join('');

      const btn = document.getElementById('save-marks-btn');
      if (btn) btn.classList.remove('d-none');
    } catch (e) {
      if (tbody) tbody.innerHTML = `<tr><td colspan="5" class="text-danger py-4 text-center">${e.message}</td></tr>`;
    }
  },

  async saveMarks() {
    const examId = parseInt(document.getElementById('marks-exam').value);
    const subjectId = parseInt(document.getElementById('marks-subject').value);

    const records = [];
    for (const s of this.currentStudents) {
      const val = document.getElementById(`marks_${s.id}`).value;
      const rem = document.getElementById(`remarks_${s.id}`).value;
      if (val !== '') {
        records.push({
          student_id: s.id,
          marks_obtained: parseFloat(val),
          max_marks: 100.0,
          remarks: rem || null
        });
      }
    }

    if (records.length === 0) {
      utils.showToast('Please enter marks for at least one student', 'warning');
      return;
    }

    try {
      await api.post('/results/bulk', {
        exam_id: examId,
        subject_id: subjectId,
        records: records
      });
      utils.showToast('Marks saved successfully!', 'success');
    } catch (e) {
      utils.showToast(e.message || 'Failed to save marks', 'danger');
    }
  },

  async loadStudentResults() {
    const container = document.getElementById('student-results-container');
    if (!container) return;

    try {
      const results = await api.get('/student/results');
      if (results.length === 0) {
        container.innerHTML = '<div class="col-12 text-muted text-center py-5">No published exam results found.</div>';
        return;
      }

      container.innerHTML = `
        <div class="table-custom-wrapper">
          <table class="table-custom">
            <thead>
              <tr>
                <th>Exam Name</th>
                <th>Subject</th>
                <th>Marks Obtained</th>
                <th>Max Marks</th>
                <th>Percentage</th>
                <th>Grade</th>
                <th>Remarks</th>
              </tr>
            </thead>
            <tbody>
              ${results.map(r => `
                <tr>
                  <td><strong>${r.exam_name}</strong></td>
                  <td>${r.subject_name}</td>
                  <td>${r.marks_obtained}</td>
                  <td>${r.max_marks}</td>
                  <td>${r.percentage}%</td>
                  <td>${utils.getGradeBadge(r.grade)}</td>
                  <td>${r.remarks || '—'}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      `;
    } catch (e) {
      container.innerHTML = `<div class="col-12 text-danger text-center py-4">${e.message}</div>`;
    }
  }
};

window.resultsManager = resultsManager;
