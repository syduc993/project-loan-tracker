import state, { setState } from '../state.js';
import { getPlanFormHtml, handlePlanSubmit } from './planUI.js';
import { getSupplierFormHtml, handleSupplierSubmit } from './supplierUI.js';
import { getInvoiceFormHtml, handleInvoiceSubmit } from './invoiceUI.js';
import { getDisbursementFormHtml, handleDisbursementSubmit } from './disbursementUI.js';

export const DOM = {
    mainListView: document.getElementById('main-list-view'),
    planDetailsView: document.getElementById('plan-details-view'),
    modal: document.getElementById('entity-modal'),
    entityForm: document.getElementById('entity-form'),
    modalTitle: document.getElementById('modal-title'),
    planManagementView: document.getElementById('plan-management-view'),
    supplierManagementView: document.getElementById('supplier-management-view'),
    navPlans: document.getElementById('nav-plans'),
    navSuppliers: document.getElementById('nav-suppliers'),
};

export function formatCurrency(amount) {
    if (amount === null || amount === undefined) return '';
    return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(amount);
}

export function formatDate(dateString) {
    if (!dateString) return '';
    return new Date(dateString + 'T00:00:00').toLocaleDateString('vi-VN');
}

export function showMainListView() {
    DOM.mainListView.style.display = 'block';
    DOM.planDetailsView.style.display = 'none';
    setState({ selectedPlan: null });
}

export function showPlanDetailsView() {
    DOM.mainListView.style.display = 'none';
    DOM.planDetailsView.style.display = 'block';
}

export function showTabInMainView(viewId) {
    if (DOM.planManagementView) DOM.planManagementView.style.display = (viewId === 'plan-management-view') ? 'block' : 'none';
    if (DOM.supplierManagementView) DOM.supplierManagementView.style.display = (viewId === 'supplier-management-view') ? 'block' : 'none';
    if (DOM.navPlans) DOM.navPlans.classList.toggle('active', viewId === 'plan-management-view');
    if (DOM.navSuppliers) DOM.navSuppliers.classList.toggle('active', viewId === 'supplier-management-view');
}

export function closeModal() {
    DOM.modal.classList.remove('visible');
    setTimeout(() => {
        DOM.modal.classList.add('hidden');
        DOM.entityForm.reset();
        setState({ currentEditingId: null, currentEntityType: null });
    }, 300);
}

export function openModal(type, entity = null) {
    setState({
        currentEntityType: type,
        currentEditingId: entity ? entity.id : null
    });
    
    let formHtml = '';
    let title = '';

    switch (type) {
        case 'plan':
            title = entity ? 'Sửa Kế hoạch' : 'Thêm Kế hoạch';
            formHtml = getPlanFormHtml(entity);
            break;
        case 'supplier':
            title = entity ? 'Sửa Nhà Cung Cấp' : 'Thêm NCC';
            formHtml = getSupplierFormHtml(entity);
            break;
        case 'invoice':
            title = entity ? 'Sửa Hóa đơn' : 'Thêm Hóa đơn';
            formHtml = getInvoiceFormHtml(entity);
            break;
        case 'disbursement':
            title = entity ? 'Sửa Giải Ngân' : 'Thêm Giải Ngân';
            formHtml = getDisbursementFormHtml(entity);
            break;

    }

    DOM.modalTitle.textContent = title;
    DOM.entityForm.innerHTML = formHtml;
    DOM.modal.classList.remove('hidden');
    setTimeout(() => DOM.modal.classList.add('visible'), 10);
}

export async function handleFormSubmit(event) {
    event.preventDefault();
    switch (state.currentEntityType) {
        case 'plan':
            await handlePlanSubmit(event.target);
            break;
        case 'supplier':
            await handleSupplierSubmit(event.target);
            break;
        case 'invoice':
            await handleInvoiceSubmit(event.target);
            break;

        case 'disbursement':
            await handleDisbursementSubmit(event.target);
            break;

    }
}