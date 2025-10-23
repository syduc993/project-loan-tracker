import { planAPI } from '../api.js';
import { closeModal } from './common.js';

const tableContainer = document.getElementById('plans-table-container');

function renderPlansTable(plans) {
    if (!plans || plans.length === 0) {
        tableContainer.innerHTML = '<p>Chưa có kế hoạch nào.</p>';
        return;
    }
    tableContainer.innerHTML = `
        <table>
            <thead><tr><th>Tên Kế hoạch</th><th>Mô tả</th><th class="actions">Hành động</th></tr></thead>
            <tbody>
                ${plans.map(p => `
                    <tr data-id="${p.id}" data-type="plan">
                        <td><a href="#" class="view-details-link">${p.name}</a></td>
                        <td>${p.description || ''}</td>
                        <td class="actions">
                            <button class="icon-btn edit-btn" title="Sửa"><span class="material-icons">edit</span></button>
                            <button class="icon-btn delete-btn" title="Xóa"><span class="material-icons">delete</span></button>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>`;
}

export async function loadPlans() {
    tableContainer.innerHTML = '<p>Đang tải...</p>';
    try {
        const plans = await planAPI.getAll();
        renderPlansTable(plans);
    } catch (e) {
        tableContainer.innerHTML = `<p style="color: red;">Lỗi tải kế hoạch: ${e.message}</p>`;
    }
}


export function getPlanFormHtml(p) {

    const idInput = p ? `<input type="hidden" name="id" value="${p.id}">` : '';

    return `
        ${idInput} 
        <div class="form-group"><label>Tên Kế hoạch *</label><input type="text" name="name" required value="${p ? p.name : ''}"></div>
        <div class="form-group"><label>Mô tả</label><textarea name="description" rows="3">${p ? p.description || '' : ''}</textarea></div>
        <div class="form-group"><label>Ngày trả lãi định kỳ *</label><input type="number" name="periodic_interest_day" required min="1" max="31" value="${p ? p.periodic_interest_day : '25'}"></div>
        
        <hr>
        <h4>Thông tin Khoản vay</h4>
        <div class="form-group"><label>Ngày thực tế vay</label><input type="date" name="actual_date" value="${p && p.actual_date ? p.actual_date : ''}"></div>
        <div class="form-group"><label>Ngày đáo hạn (trả gốc)</label><input type="date" name="principal_due_date" value="${p && p.principal_due_date ? p.principal_due_date : ''}"></div>
        <div class="form-group"><label>Ngân hàng</label><input type="text" name="bank_name" value="${p ? p.bank_name || '' : ''}"></div>
        <div class="form-group"><label>Số HĐ Tín dụng</label><input type="text" name="loan_contract_number" value="${p ? p.loan_contract_number || '' : ''}"></div>

        <div class="modal-footer"><button type="submit" class="btn btn-primary">Lưu</button></div>
    `;
}

export async function handlePlanSubmit(form) {
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    // Lấy ID từ form data
    const id = data.id;

    // Chuyển đổi các trường date rỗng thành null để API không báo lỗi
    const dateFields = ['actual_date', 'principal_due_date'];
    dateFields.forEach(field => {
        if (data[field] === '') {
            data[field] = null;
        }
    });

    try {
        if (id) {
            // Đã có id, gọi API update
            await planAPI.update(id, data);
        } else {
            // Không có id, gọi API create
            await planAPI.create(data);
        }
        closeModal();
        loadPlans();
    } catch (error) {
        alert(`Lỗi: ${error.message}`);
    }
}