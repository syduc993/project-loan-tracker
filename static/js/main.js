import state, { setState } from './state.js';
import { planAPI, supplierAPI, invoiceAPI, disbursementAPI } from './api.js';
import { DOM, showMainListView, showPlanDetailsView, showTabInMainView, openModal, closeModal, handleFormSubmit } from './ui/common.js';
import { loadPlans } from './ui/planUI.js';
import { loadSuppliers, loadSuppliersCache } from './ui/supplierUI.js';
import { loadInvoices, changeInvoicePage } from './ui/invoiceUI.js';
import { loadDisbursements } from './ui/disbursementUI.js';

// --- MAIN FUNCTION TO LOAD PLAN DETAILS ---
export async function loadPlanDetails(planId) {
    showPlanDetailsView();
    const planDetailsTitle = document.getElementById('plan-details-title');
    const planDetailsDescription = document.getElementById('plan-details-description');
    
    planDetailsTitle.textContent = "Đang tải chi tiết kế hoạch...";
    planDetailsDescription.textContent = "";

    try {
        const planData = await planAPI.getById(planId);
        setState({ selectedPlan: planData });
        
        planDetailsTitle.textContent = `Chi tiết cho Kế hoạch: ${planData.name}`;
        planDetailsDescription.textContent = planData.description || '';
        
        // Tải hóa đơn và giải ngân song song
        await Promise.all([
            loadInvoices(planId),
            loadDisbursements(planId)
        ]);

    } catch (e) {
        planDetailsTitle.textContent = "Lỗi tải chi tiết kế hoạch";
        console.error(e);
    }
}

// --- EVENT LISTENERS ---
function setupEventListeners() {
    // Navigation
    DOM.navPlans.addEventListener('click', () => {
        showMainListView();
        showTabInMainView('plan-management-view');
        loadPlans();
    });

    DOM.navSuppliers.addEventListener('click', () => {
        showMainListView();
        showTabInMainView('supplier-management-view');
        loadSuppliers();
    });

    document.getElementById('back-to-list-btn').addEventListener('click', () => {
        showMainListView();
        showTabInMainView('plan-management-view');
        loadPlans();
    });

    // Add buttons
    document.getElementById('add-plan-btn').addEventListener('click', () => openModal('plan'));
    document.getElementById('add-supplier-btn').addEventListener('click', () => openModal('supplier'));
    document.getElementById('add-invoice-btn').addEventListener('click', () => openModal('invoice'));
    document.getElementById('add-disbursement-btn').addEventListener('click', () => openModal('disbursement'));

    // Modal
    document.getElementById('close-modal-btn').addEventListener('click', closeModal);
    DOM.modal.addEventListener('click', e => { if(e.target === DOM.modal) closeModal(); });
    DOM.entityForm.addEventListener('submit', handleFormSubmit);

    document.getElementById('generate-schedule-btn-auto').addEventListener('click', async () => {
        if (!state.selectedPlan || !state.selectedPlan.id) return;
        const plan = state.selectedPlan;
        if (confirm(`Tạo/Cập nhật lịch trả lãi cho kế hoạch "${plan.name}"? Lịch cũ (nếu có) sẽ bị xóa.`)) {
            try {
                const result = await planAPI.generateSchedule(plan.id);
                alert(result.message);
                loadPlanDetails(plan.id);
            } catch (e) { alert(`Lỗi: ${e.message}`); }
        }
    });

    document.getElementById('delete-schedule-btn-auto').addEventListener('click', async () => {
        if (!state.selectedPlan || !state.selectedPlan.id) return;
        const plan = state.selectedPlan;
        if (confirm(`Xóa toàn bộ lịch trả lãi của kế hoạch "${plan.name}"?`)) {
            try {
                const result = await planAPI.deleteSchedule(plan.id);
                alert(result.message);
                loadPlanDetails(plan.id);
            } catch (e) { alert(`Lỗi: ${e.message}`); }
        }
    });


    // Delegated events for tables
    document.body.addEventListener('click', async (event) => {
        const target = event.target;
        
        // View plan details
        if (target.matches('.view-details-link')) {
            event.preventDefault();
            loadPlanDetails(target.closest('tr').dataset.id);
        }

        // Pagination for invoices
        const paginationBtn = target.closest('.pagination-btn');
        if (paginationBtn) {
            changeInvoicePage(parseInt(paginationBtn.dataset.page));
        }

        // Generic Edit/Delete buttons
        const iconBtn = target.closest('.icon-btn');
        if (iconBtn) {
            const row = iconBtn.closest('tr');
            if(!row) return;

            const id = row.dataset.id;
            const type = row.dataset.type;

            if (iconBtn.classList.contains('edit-btn')) {
                try {
                    let data;
                    if (type === 'plan') data = await planAPI.getById(id);
                    else if (type === 'supplier') data = await supplierAPI.getById(id);
                    else if (type === 'invoice') data = await invoiceAPI.getById(id);
                    else if (type === 'disbursement') data = await disbursementAPI.getById(id);
                    
                    if(data) openModal(type, data);

                } catch(e) { alert(e.message); }
            }
            
            if (iconBtn.classList.contains('delete-btn')) {
                if (confirm(`Bạn chắc chắn muốn xóa mục (ID: ${id}) này?`)) {
                    try {
                        if (type === 'plan') await planAPI.delete(id);
                        else if (type === 'supplier') { await supplierAPI.delete(id); loadSuppliersCache(); }
                        else if (type === 'invoice') await invoiceAPI.delete(id);
                        else if (type === 'disbursement') await disbursementAPI.delete(id);
                        
                        // Reload relevant data
                        if (type === 'plan' || type === 'supplier') {
                             loadPlans();
                             loadSuppliers();
                        }
                        else if (type === 'invoice' || type === 'disbursement') {
                            loadPlanDetails(state.selectedPlan.id);
                        }

                    } catch(e) { alert(e.message); }
                }
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    showMainListView();
    showTabInMainView('plan-management-view');
    loadPlans();
    loadSuppliersCache();
});