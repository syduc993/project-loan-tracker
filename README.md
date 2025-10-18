-- Bảng 1: Nhà Cung Cấp
CREATE TABLE suppliers (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name TEXT NOT NULL,
    contact_info TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Bảng 2: Kế Hoạch Giải Ngân
CREATE TABLE disbursement_plans (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Bảng 3: Hóa Đơn (liên kết với Kế hoạch)
CREATE TABLE invoices (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    plan_id BIGINT REFERENCES disbursement_plans(id) ON DELETE CASCADE,
    supplier_id BIGINT REFERENCES suppliers(id) ON DELETE SET NULL,
    invoice_number TEXT NOT NULL,
    issue_date DATE NOT NULL,
    total_value NUMERIC(15, 2) NOT NULL,
    status TEXT DEFAULT 'Chưa thanh toán',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Bảng 4: Các Lần Giải Ngân (liên kết với Kế hoạch)
-- THAY ĐỔI QUAN TRỌNG: Liên kết trực tiếp với plan_id
CREATE TABLE disbursements (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    plan_id BIGINT REFERENCES disbursement_plans(id) ON DELETE CASCADE,
    
    -- Kế hoạch và thực tế
    planned_date DATE,
    planned_amount NUMERIC(15, 2),
    actual_date DATE,
    actual_amount NUMERIC(15, 2),

    -- Thông tin tài chính & khế ước
    bank_name TEXT,
    loan_contract_number TEXT,
    loan_term_months INT,
    loan_interest_rate REAL,
    interest_amount NUMERIC(15, 2),
    interest_due_date DATE,
    principal_due_date DATE,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

