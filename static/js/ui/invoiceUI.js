// File: static/js/ui/invoiceUI.js
// Logic UI cho Hóa đơn

import { invoiceAPI } from '../api.js';
import state, { setState } from '../state.js';
import { formatCurrency, formatDate, closeModal } from './common.js';
import { loadPlanDetails } from '../main.js'; // Import hàm load chính

const tableContainer = document.getElementById('invoices-table-container');

function renderInvoicesTable() {
    const { allInvoices, currentPage, invoicesPerPage } = state.invoicePagination;

    if (!allInvoices || allInvoices.length === 0) {
        tableContainer.innerHTML = '<p>Chưa có hóa đơn nào cho kế hoạch này.</p>';
        return;
    }
    
    const totalValue = allInvoices.reduce((sum, inv) => sum + parseFloat(inv.total_value || 0), 0);
    const totalPages = Math.ceil(allInvoices.length / invoicesPerPage);
    const paginatedInvoices = allInvoices.slice((currentPage - 1) * invoicesPerPage, currentPage * invoicesPerPage);
    
    // Nút phân trang được tạo dưới dạng chuỗi HTML để dễ dàng gán sự kiện sau này
    const paginationControls = totalPages > 1 ? `
        <div class="pagination" style="margin-top: 16px; text-align: center; display: flex; align-items: center; justify-content: center; gap: 16px;">
            <button class="btn btn-secondary pagination-btn" data-page="${currentPage - 1}" ${currentPage === 1 ? 'disabled' : ''}>Trước</button>
            <span style="font-weight: 500;">Trang ${currentPage} / ${totalPages}</span>
            <button class="btn btn-secondary pagination-btn" data-page="${currentPage + 1}" ${currentPage === totalPages ? 'disabled' : ''}>Sau</button>
        </div>` : '';

    tableContainer.innerHTML = `
        <table>
            <thead><tr><th>Số HĐ</th><th>Ngày HĐ</th><th>NCC</th><th>Giá trị</th><th class="actions">Hành động</th></tr></thead>
            <tbody>
            ${paginatedInvoices.map(inv => `
                <tr data-id="${inv.id}" data-type="invoice">
                    <td>${inv.invoice_number}</td><td>${formatDate(inv.issue_date)}</td>
                    <td>${inv.supplier?.name || 'N/A'}</td><td>${formatCurrency(inv.total_value)}</td>
                    <td class="actions">
                        <button class="icon-btn edit-btn" title="Sửa"><span class="material-icons">edit</span></button>
                        <button class="icon-btn delete-btn" title="Xóa"><span class="material-icons">delete</span></button>
                    </td>
                </tr>`).join('')}
            </tbody>
            <tfoot>
                <tr style="font-weight: bold; background-color: #f5f5f5;">
                    <td colspan="3" style="text-align: right;">Tổng cộng:</td>
                    <td>${formatCurrency(totalValue)}</td><td></td>
                </tr>
            </tfoot>
        </table>
        ${paginationControls}`;
}

export function changeInvoicePage(newPage) {
    const { allInvoices, invoicesPerPage } = state.invoicePagination;
    const totalPages = Math.ceil(allInvoices.length / invoicesPerPage);
    if (newPage >= 1 && newPage <= totalPages) {
        setState({ invoicePagination: { ...state.invoicePagination, currentPage: newPage } });
        renderInvoicesTable();
    }
}

export async function loadInvoices(planId) {
    tableContainer.innerHTML = '<p>Đang tải hóa đơn...</p>';
    try {
        const invoices = await invoiceAPI.getByPlanId(planId);
        setState({ invoicePagination: { ...state.invoicePagination, allInvoices: invoices, currentPage: 1 } });
        renderInvoicesTable();
    } catch (e) {
        tableContainer.innerHTML = `<p style="color: red;">Lỗi tải hóa đơn: ${e.message}</p>`;
    }
}

export function getInvoiceFormHtml(inv) {
    const supplierOptions = state.suppliersCache.map(s => 
        `<option value="${s.id}" ${inv && inv.supplier_id === s.id ? 'selected' : ''}>${s.name}</option>`
    ).join('');

    return `
        <input type="hidden" name="plan_id" value="${state.selectedPlan.id}">
        <div class="form-group"><label>Số hóa đơn *</label><input type="text" name="invoice_number" required value="${inv ? inv.invoice_number : ''}"></div>
        <div class="form-group"><label>Ngày hóa đơn *</label><input type="date" name="issue_date" required value="${inv ? inv.issue_date : ''}"></div>
        <div class="form-group"><label>Giá trị *</label><input type="number" step="any" name="total_value" required value="${inv ? inv.total_value : ''}"></div>
        <div class="form-group"><label>Nhà cung cấp *</label><select name="supplier_id" required>${supplierOptions}</select></div>
        <div class="form-group"><label>Trạng thái</label>
            <select name="status">
                <option value="Chưa thanh toán" ${inv && inv.status === 'Chưa thanh toán' ? 'selected' : ''}>Chưa thanh toán</option>
                <option value="Đã thanh toán" ${inv && inv.status === 'Đã thanh toán' ? 'selected' : ''}>Đã thanh toán</option>
            </select>
        </div>
        <div class="modal-footer"><button type="submit" class="btn btn-primary">Lưu</button></div>
    `;
}

export async function handleInvoiceSubmit(form) {
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    const id = state.currentEditingId;

    try {
        if (id) {
            await invoiceAPI.update(id, data);
        } else {
            await invoiceAPI.create(data);
        }
        closeModal();
        loadPlanDetails(state.selectedPlan.id); // Tải lại toàn bộ chi tiết kế hoạch
    } catch (error) {
        alert(`Lỗi: ${error.message}`);
    }
}