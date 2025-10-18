document.addEventListener('DOMContentLoaded', function() {
    const plansContainer = document.getElementById('plans-container');
    const detailsSection = document.getElementById('details-section');
    const invoicesContainer = document.getElementById('invoices-container');
    const disbursementsContainer = document.getElementById('disbursements-container');
    const planNameSpan = document.getElementById('plan-name');
    
    const formatCurrency = (value) => value != null ? new Intl.NumberFormat('vi-VN').format(value) : 'N/A';
    const formatDate = (value) => value ? new Date(value).toLocaleDateString('vi-VN') : 'N/A';

    // 1. Hiển thị danh sách các Kế hoạch
    async function displayPlans() {
        try {
            const response = await fetch('/api/v1/plans');
            const plans = await response.json();
            let html = '<ul>';
            plans.forEach(plan => {
                html += `<li><a href="#" class="plan-link" data-id="${plan.id}" data-name="${plan.name}">${plan.name}</a></li>`;
            });
            html += '</ul>';
            plansContainer.innerHTML = html;

            document.querySelectorAll('.plan-link').forEach(link => {
                link.addEventListener('click', handlePlanClick);
            });
        } catch (error) {
            plansContainer.innerHTML = '<p style="color:red;">Lỗi tải danh sách kế hoạch.</p>';
        }
    }

    // 2. Xử lý khi click vào một Kế hoạch
    async function handlePlanClick(event) {
        event.preventDefault();
        const planId = event.target.dataset.id;
        const planName = event.target.dataset.name;
        
        planNameSpan.textContent = planName;
        detailsSection.style.display = 'block';
        invoicesContainer.innerHTML = '<p>Đang tải hóa đơn...</p>';
        disbursementsContainer.innerHTML = '<p>Đang tải chi tiết giải ngân...</p>';
        
        // Gọi cả hai hàm để tải dữ liệu song song
        await Promise.all([
            displayInvoices(planId),
            displayDisbursements(planId)
        ]);
    }

    // 3. Hiển thị Hóa đơn cho một Kế hoạch
    async function displayInvoices(planId) {
        const response = await fetch(`/api/v1/invoices/plan/${planId}`);
        const invoices = await response.json();

        if (invoices.length === 0) {
            invoicesContainer.innerHTML = '<p>Kế hoạch này chưa có hóa đơn.</p>';
            return;
        }

        let table = `<table><thead><tr><th>Số HĐ</th><th>Ngày HĐ</th><th>NCC</th><th>Giá trị</th><th>Trạng thái</th></tr></thead><tbody>`;
        invoices.forEach(inv => {
            table += `<tr>
                <td>${inv.invoice_number}</td>
                <td>${formatDate(inv.issue_date)}</td>
                <td>${inv.suppliers ? inv.suppliers.name : 'N/A'}</td>
                <td>${formatCurrency(inv.total_value)}</td>
                <td>${inv.status}</td>
            </tr>`;
        });
        table += '</tbody></table>';
        invoicesContainer.innerHTML = table;
    }

    // 4. Hiển thị các Lần Giải ngân cho một Kế hoạch
    async function displayDisbursements(planId) {
        const response = await fetch(`/api/v1/disbursements/plan/${planId}`);
        const disbursements = await response.json();

        if (disbursements.length === 0) {
            disbursementsContainer.innerHTML = '<p>Kế hoạch này chưa có lần giải ngân nào.</p>';
            return;
        }
        
        let cumulativeAmount = 0;
        let table = `<table><thead><tr>
            <th>Ngày GN thực tế</th><th>Giá trị GN</th><th>Lũy kế</th><th>Ngân hàng</th><th>Số khế ước</th><th>Lãi suất</th><th>Ngày đáo hạn</th>
        </tr></thead><tbody>`;

        disbursements.forEach(d => {
            cumulativeAmount += d.actual_amount || 0;
            table += `<tr>
                <td>${formatDate(d.actual_date)}</td>
                <td>${formatCurrency(d.actual_amount)}</td>
                <td>${formatCurrency(cumulativeAmount)}</td>
                <td>${d.bank_name || 'N/A'}</td>
                <td>${d.loan_contract_number || 'N/A'}</td>
                <td>${d.loan_interest_rate ? (d.loan_interest_rate * 100).toFixed(2) + '%' : 'N/A'}</td>
                <td>${formatDate(d.principal_due_date)}</td>
            </tr>`;
        });
        table += '</tbody></table>';
        disbursementsContainer.innerHTML = table;
    }

    // Bắt đầu chạy
    displayPlans();
});