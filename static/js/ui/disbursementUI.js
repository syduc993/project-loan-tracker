import { disbursementAPI } from '../api.js';
import state, { setState } from '../state.js';
import { formatCurrency, formatDate, closeModal } from './common.js';
import { loadPlanDetails } from '../main.js';

const tableContainer = document.getElementById('disbursements-table-container');

function renderDisbursementsTable(disbursements) {
    if (!disbursements || disbursements.length === 0) {
        tableContainer.innerHTML = '<p>Chưa có lịch trả lãi nào. Hãy nhấn "Tạo Lịch Tự Động".</p>';
        return;
    }

    const totalInterestAmount = disbursements.reduce((sum, d) => sum + parseFloat(d.interest_amount || 0), 0);

    let tableHtml = `
        <table>
            <thead>
                <tr>
                    <th>Ngày đến hạn trả lãi</th>
                    <th>Số tiền lãi</th>
                    <th>Ngày thực trả</th>
                    <th class="actions">Hành động</th>
                </tr>
            </thead>
            <tbody>`;

    disbursements.sort((a,b) => new Date(a.interest_due_date) - new Date(b.interest_due_date)).forEach(d => {
        tableHtml += `
            <tr data-id="${d.id}" data-type="disbursement">
                <td>${formatDate(d.interest_due_date)}</td>
                <td>${formatCurrency(d.interest_amount)}</td>
                <td>${formatDate(d.actual_date)}</td>
                <td class="actions">
                    <button class="icon-btn edit-btn" title="Cập nhật trả lãi"><span class="material-icons">edit</span></button>
                    <button class="icon-btn delete-btn" title="Xóa"><span class="material-icons">delete</span></button>
                </td>
            </tr>`;
    });
    
    tableHtml += `</tbody>
        <tfoot>
            <tr style="font-weight: bold; background-color: #f5f5f5;">
                <td style="text-align: right;">Tổng lãi đã trả:</td>
                <td>${formatCurrency(totalInterestAmount)}</td>
                <td colspan="2"></td>
            </tr>
        </tfoot>
    </table>`;
    tableContainer.innerHTML = tableHtml;
}

export async function loadDisbursements(planId) {
    tableContainer.innerHTML = '<p>Đang tải lịch trả lãi...</p>';
    try {
        const disbursements = await disbursementAPI.getByPlanId(planId);
        renderDisbursementsTable(disbursements);
    } catch (e) {
        tableContainer.innerHTML = `<p style="color: red;">Lỗi tải lịch trả lãi: ${e.message}</p>`;
    }
}

// Hàm tạo HTML cho form
export function getDisbursementFormHtml(d) {
    return `
        <input type="hidden" name="plan_id" value="${d ? d.plan_id : state.selectedPlan.id}">
        
        <div class="form-group">
            <label>Ngày đến hạn trả lãi *</label>
            <input type="date" name="interest_due_date" required value="${d?.interest_due_date || ''}">
        </div>
        <div class="form-group">
            <label>Số tiền lãi</label>
            <input type="number" step="any" name="interest_amount" placeholder="Để trống nếu chưa có" value="${d?.interest_amount || ''}">
        </div>
        <div class="form-group">
            <label>Ngày thực trả</label>
            <input type="date" name="actual_date" value="${d?.actual_date || ''}">
        </div>

        <div class="modal-footer"><button type="submit" class="btn btn-primary">Lưu</button></div>
    `;
}

// Hàm xử lý submit form
export async function handleDisbursementSubmit(form) {
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    const id = state.currentEditingId;

    // Chuyển đổi các trường số và null nếu rỗng
    const fieldsToConvert = ['interest_amount'];
    for (const key of fieldsToConvert) {
        if (data[key] === '' || data[key] === null) {
            data[key] = null;
        } else {
            data[key] = Number(data[key]);
        }
    }
    // Chuyển đổi ngày rỗng
    const dateFields = ['interest_due_date', 'actual_date'];
    for (const key of dateFields) {
        if (data[key] === '') {
            data[key] = null;
        }
    }

    try {
        if (id) {
            // Khi cập nhật, chỉ gửi các trường được phép trong schema Update
            const updateData = {
                interest_due_date: data.interest_due_date,
                interest_amount: data.interest_amount,
                actual_date: data.actual_date
            };
            await disbursementAPI.update(id, updateData);
        } else {
            await disbursementAPI.create(data);
        }
        closeModal();
        loadPlanDetails(state.selectedPlan.id);
    } catch (error) {
        alert(`Lỗi: ${error.message}`);
    }
}