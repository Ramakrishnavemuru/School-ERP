/**
 * Reports Controller
 */
const reportsManager = {
  attendanceChartInstance: null,
  academicChartInstance: null,

  async init() {
    await this.loadAttendanceReport();
    await this.loadFeeReport();
    await this.loadAcademicReport();
  },

  async loadAttendanceReport() {
    try {
      const data = await api.get('/reports/attendance');
      const setText = (id, val) => {
        const el = document.getElementById(id);
        if (el) el.textContent = val;
      };

      setText('rep-att-total', data.total_records || 0);
      setText('rep-att-pct', `${data.percentage || 0}%`);
      setText('rep-att-present', data.present || 0);
      setText('rep-att-absent', data.absent || 0);

      const canvas = document.getElementById('reportAttendanceChart');
      if (canvas && window.Chart) {
        if (this.attendanceChartInstance) this.attendanceChartInstance.destroy();
        this.attendanceChartInstance = new Chart(canvas, {
          type: 'pie',
          data: {
            labels: ['Present', 'Absent', 'Late'],
            datasets: [{
              data: [data.present || 0, data.absent || 0, data.late || 0],
              backgroundColor: ['#10b981', '#ef4444', '#f59e0b']
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false
          }
        });
      }
    } catch (e) {
      console.error(e);
    }
  },

  async loadFeeReport() {
    try {
      const data = await api.get('/reports/fees');
      const setText = (id, val) => {
        const el = document.getElementById(id);
        if (el) el.textContent = val;
      };

      setText('rep-fee-expected', utils.formatCurrency(data.total_fees_expected || 0));
      setText('rep-fee-collected', utils.formatCurrency(data.total_collected || 0));
      setText('rep-fee-outstanding', utils.formatCurrency(data.total_outstanding || 0));
    } catch (e) {
      console.error(e);
    }
  },

  async loadAcademicReport() {
    try {
      const data = await api.get('/reports/academic');
      const setText = (id, val) => {
        const el = document.getElementById(id);
        if (el) el.textContent = val;
      };

      setText('rep-acad-avg', `${data.average_percentage || 0}%`);
      setText('rep-acad-total', data.total_results || 0);

      const canvas = document.getElementById('reportAcademicChart');
      if (canvas && window.Chart && data.grades_breakdown) {
        if (this.academicChartInstance) this.academicChartInstance.destroy();
        const labels = Object.keys(data.grades_breakdown);
        const counts = Object.values(data.grades_breakdown);

        this.academicChartInstance = new Chart(canvas, {
          type: 'bar',
          data: {
            labels: labels.length > 0 ? labels : ['A+', 'A', 'B', 'C', 'D', 'F'],
            datasets: [{
              label: 'Students Count',
              data: counts.length > 0 ? counts : [0, 0, 0, 0, 0, 0],
              backgroundColor: '#2563eb'
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: { beginAtZero: true, ticks: { stepSize: 1 } }
            }
          }
        });
      }
    } catch (e) {
      console.error(e);
    }
  }
};

window.reportsManager = reportsManager;
