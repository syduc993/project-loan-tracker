import { supplierAPI } from '../api.js';
import { closeModal } from './common.js';
import state, { setState } from '../state.js';

const tableContainer = document.getElementById('suppliers-table-container');

function renderSuppliersTable(suppliers) {
    if (!suppliers || suppliers.length === 0) {
        tableContainer.innerHTML = '<p>Chưa có nhà cung cấp nào.</p>';
        return;
    }
    tableContainer.innerHTML = `
        <table>
            <thead><tr><th>Tên NCC</th><th>Liên hệ</th><th class="actions">Hành động</th></tr></thead>
            <tbody>
                ${suppliers.map(s => `
                    <tr data-id="${s.id}" data-type="supplier">
                        <td>${s.name}</td>
                        <td>${s.contact_info || ''}</td>
                        <td class="actions">
                            <button class="icon-btn edit-btn" title="Sửa"><span class="material-icons">edit</span></button>
                            <button class="icon-btn delete-btn" title="Xóa"><span class="material-icons">delete</span></button>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>`;
}

export async function loadSuppliers() {
    tableContainer.innerHTML = '<p>Đang tải...</p>';
    try {
        const suppliers = await supplierAPI.getAll();
        renderSuppliersTable(suppliers);
    } catch (e) {
        tableContainer.innerHTML = `<p style="color: red;">Lỗi tải NCC: ${e.message}</p>`;
    }
}

export async function loadSuppliersCache() {
    try {
        const suppliers = await supplierAPI.getAll();
        setState({ suppliersCache: suppliers });
    } catch(e) { 
        console.error("Lỗi tải cache NCC:", e); 
    }
}

export function getSupplierFormHtml(s) {
    return `
        <div class="form-group"><label>Tên NCC *</label><input type="text" name="name" required value="${s ? s.name : ''}"></div>
        <div class="form-group"><label>Liên hệ</label><textarea name="contact_info" rows="3">${s ? s.contact_info || '' : ''}</textarea></div>
        <div class="modal-footer"><button type="submit" class="btn btn-primary">Lưu</button></div>
    `;
}

export async function handleSupplierSubmit(form) {
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    const id = state.currentEditingId;

    try {
        if (id) {
            await supplierAPI.update(id, data);
        } else {
            await supplierAPI.create(data);
        }
        closeModal();
        loadSuppliers();
        loadSuppliersCache(); // Cập nhật lại cache
    } catch (error) {
        alert(`Lỗi: ${error.message}`);
    }
}