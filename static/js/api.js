async function fetchAPI(endpoint, options = {}) {
    const headers = { 'Content-Type': 'application/json', ...options.headers };
    const response = await fetch(`/api/v1/${endpoint}`, { ...options, headers });
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Có lỗi xảy ra');
    }
    if (response.status === 204) return null;
    return response.json();
}

export const planAPI = {
    getAll: () => fetchAPI('plans/'),
    getById: (id) => fetchAPI(`plans/${id}`),
    create: (data) => fetchAPI('plans/', { method: 'POST', body: JSON.stringify(data) }),
    update: (id, data) => fetchAPI(`plans/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    delete: (id) => fetchAPI(`plans/${id}`, { method: 'DELETE' }),
    generateSchedule: (planId) => fetchAPI(`plans/${planId}/generate-interest-schedule`, { method: 'POST' }),
    deleteSchedule: (planId) => fetchAPI(`plans/${planId}/interest-schedule`, { method: 'DELETE' }),
};

export const supplierAPI = {
    getAll: () => fetchAPI('suppliers/'),
    getById: (id) => fetchAPI(`suppliers/${id}`),
    create: (data) => fetchAPI('suppliers/', { method: 'POST', body: JSON.stringify(data) }),
    update: (id, data) => fetchAPI(`suppliers/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    delete: (id) => fetchAPI(`suppliers/${id}`, { method: 'DELETE' }),
};

export const invoiceAPI = {
    getByPlanId: (planId) => fetchAPI(`invoices/plan/${planId}`),
    getById: (id) => fetchAPI(`invoices/${id}`),
    create: (data) => fetchAPI('invoices/', { method: 'POST', body: JSON.stringify(data) }),
    update: (id, data) => fetchAPI(`invoices/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    delete: (id) => fetchAPI(`invoices/${id}`, { method: 'DELETE' }),
};

export const disbursementAPI = {
    getByPlanId: (planId) => fetchAPI(`disbursements/plan/${planId}`),
    getById: (id) => fetchAPI(`disbursements/${id}`),
    create: (data) => fetchAPI('disbursements/', { method: 'POST', body: JSON.stringify(data) }),
    update: (id, data) => fetchAPI(`disbursements/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    delete: (id) => fetchAPI(`disbursements/${id}`, { method: 'DELETE' }),
};