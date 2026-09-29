/**
 * Fees & Payments Controller
 */
const feesManager = {
  async initAdmin() {
    await this.loadClassSelect();
    await this.loadFeeStructures();
    await this.loadPayments();
  },

  async loadClassSelect() {
    const sel = document.getElementById('fee-class-id');
    const payFeeSel = document.getElementById('payment-fee-id');
    try {
      const classes = await api.get('/classes');
      if (sel) {
        sel.innerHTML = '<option value="">All Classes</option>' +
          classes.map(c => `<option value="${c.id}">${c.name}</option>`).join('');
      }

      const fees = await api.get('/fees');
      if (payFeeSel) {
        payFeeSel.innerHTML = '<option value="">Select Fee Structure</option>' +
          fees.map(f => `<option value="${f.id}">${f.title} (${utils.formatCurrency(f.amount)})</option>`).join('');
      }
    } catch (e) {
      console.error(e);
    }
  },

  async loadFeeStructures() {
    const tbody = document.getElementById('fees-table-body');
    if (!tbody) return;

    try {
      const fees = await api.get('/fees');
      if (fees.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="table-empty-state">No fee structures configured.</td></tr>';
        return;
      }

      tbody.innerHTML = fees.map(f => `
        <tr>
          <td><strong>${f.title}</strong></td>
          <td><span class="badge bg-secondary">${f.fee_type}</span></td>
          <td>${f.class_name || 'All Classes'}</td>
          <td><strong>${utils.formatCurrency(f.amount)}</strong></td>
          <td>${utils.formatDate(f.due_date)}</td>
          <td>
            <button class="table-action-btn text-danger" onclick="feesManager.deleteFee(${f.id})">🗑️</button>
          </td>
        </tr>
      `).join('');
    } catch (e) {
      tbody.innerHTML = `<tr><td colspan="6" class="text-danger text-center py-3">${e.message}</td></tr>`;
    }
  },

  async createFee(formEvent) {
    if (formEvent) formEvent.preventDefault();
    const form = document.getElementById('create-fee-form');
    if (!form) return;

    const payload = {
      title: form.title.value.trim(),
      fee_type: form.fee_type.value,
      class_id: parseInt(form.class_id.value) || null,
      amount: parseFloat(form.amount.value),
      due_date: form.due_date.value,
      description: form.description.value.trim() || null
    };

    try {
      await api.post('/fees', payload);
      utils.showToast('Fee structure added successfully!', 'success');
      form.reset();
      const modalEl = document.getElementById('createFeeModal');
      if (modalEl && window.bootstrap) {
        const modal = bootstrap.Modal.getInstance(modalEl);
        if (modal) modal.hide();
      }
      this.loadFeeStructures();
      this.loadClassSelect();
    } catch (e) {
      utils.showToast(e.message || 'Failed to add fee', 'danger');
    }
  },

  async deleteFee(id) {
    if (!confirm('Are you sure you want to delete this fee structure?')) return;
    try {
      await api.delete(`/fees/${id}`);
      utils.showToast('Fee structure deleted', 'success');
      this.loadFeeStructures();
    } catch (e) {
      utils.showToast(e.message, 'danger');
    }
  },

  async loadPayments() {
    const tbody = document.getElementById('payments-table-body');
    if (!tbody) return;

    try {
      const payments = await api.get('/fees/payments');
      if (payments.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="table-empty-state">No payment records found.</td></tr>';
        return;
      }

      tbody.innerHTML = payments.map(p => `
        <tr>
          <td><strong>${p.admission_number || '—'}</strong></td>
          <td>${p.student_name || '—'}</td>
          <td>${p.fee_title || '—'}</td>
          <td class="text-success fw-bold">${utils.formatCurrency(p.amount_paid)}</td>
          <td>${utils.formatDate(p.payment_date)} (${p.payment_method})</td>
          <td>${utils.getStatusBadge(p.payment_status)}</td>
        </tr>
      `).join('');
    } catch (e) {
      tbody.innerHTML = `<tr><td colspan="6" class="text-danger text-center py-3">${e.message}</td></tr>`;
    }
  },

  async recordPayment(formEvent) {
    if (formEvent) formEvent.preventDefault();
    const form = document.getElementById('record-payment-form');
    if (!form) return;

    const payload = {
      fee_id: parseInt(form.fee_id.value),
      student_id: parseInt(form.student_id.value),
      amount_paid: parseFloat(form.amount_paid.value),
      payment_date: form.payment_date.value || null,
      payment_method: form.payment_method.value,
      payment_status: 'PAID',
      transaction_id: form.transaction_id.value.trim() || null,
      remarks: form.remarks.value.trim() || null
    };

    try {
      await api.post('/fees/payments', payload);
      utils.showToast('Payment recorded successfully!', 'success');
      form.reset();
      const modalEl = document.getElementById('recordPaymentModal');
      if (modalEl && window.bootstrap) {
        const modal = bootstrap.Modal.getInstance(modalEl);
        if (modal) modal.hide();
      }
      this.loadPayments();
    } catch (e) {
      utils.showToast(e.message || 'Failed to record payment', 'danger');
    }
  },

  async loadStudentFees() {
    const container = document.getElementById('student-fees-container');
    if (!container) return;

    try {
      const summary = await api.get('/student/fees');
      const setText = (id, val) => {
        const el = document.getElementById(id);
        if (el) el.textContent = val;
      };

      setText('fee-summary-total', utils.formatCurrency(summary.total_fees));
      setText('fee-summary-paid', utils.formatCurrency(summary.total_paid));
      setText('fee-summary-balance', utils.formatCurrency(summary.remaining_balance));

      const tbody = document.getElementById('student-fees-tbody');
      if (tbody && summary.items) {
        if (summary.items.length === 0) {
          tbody.innerHTML = '<tr><td colspan="6" class="table-empty-state">No fee dues assigned.</td></tr>';
          return;
        }

        tbody.innerHTML = summary.items.map(item => `
          <tr>
            <td><strong>${item.title}</strong></td>
            <td><span class="badge bg-secondary">${item.fee_type}</span></td>
            <td>${utils.formatCurrency(item.total_amount)}</td>
            <td class="text-success font-weight-bold">${utils.formatCurrency(item.amount_paid)}</td>
            <td class="text-danger font-weight-bold">${utils.formatCurrency(item.balance)}</td>
            <td>${utils.getStatusBadge(item.status)}</td>
          </tr>
        `).join('');
      }
    } catch (e) {
      container.innerHTML = `<div class="text-danger py-4 text-center">${e.message}</div>`;
    }
  }
};

window.feesManager = feesManager;
