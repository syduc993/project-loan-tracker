const state = {
    currentEditingId: null,
    currentEntityType: null,
    selectedPlan: null,
    
    // Cache
    suppliersCache: [],
    
    // Pagination cho hóa đơn
    invoicePagination: {
        currentPage: 1,
        invoicesPerPage: 5,
        allInvoices: []
    }
};

export function setState(newState) {
    Object.assign(state, newState);
}

export default state;