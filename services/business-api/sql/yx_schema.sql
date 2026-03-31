-- 医小管(Yixiaoguan) PostgreSQL 表结构设计
-- 依据 docs/database/schema-phase1.md

-- ==========================================
-- 1. yx_user
-- ==========================================
CREATE TABLE yx_user (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    username VARCHAR(64) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    real_name VARCHAR(50) NOT NULL,
    nickname VARCHAR(50),
    gender SMALLINT DEFAULT 0,
    phone VARCHAR(20),
    email VARCHAR(128),
    avatar_url VARCHAR(512),
    bio TEXT,
    student_id VARCHAR(32),
    employee_id VARCHAR(32),
    department VARCHAR(100),
    major VARCHAR(100),
    class_name VARCHAR(50),
    grade VARCHAR(20),
    wechat_openid VARCHAR(128) UNIQUE,
    status SMALLINT NOT NULL DEFAULT 2,
    password_changed BOOLEAN NOT NULL DEFAULT FALSE,
    last_login_at TIMESTAMP WITH TIME ZONE,
    last_login_ip VARCHAR(128),
    remark VARCHAR(500)
);

CREATE UNIQUE INDEX idx_yx_user_username ON yx_user(username);
CREATE INDEX idx_yx_user_student_id ON yx_user(student_id);
CREATE INDEX idx_yx_user_dept_class ON yx_user(department, class_name);
CREATE UNIQUE INDEX idx_yx_user_wechat_openid ON yx_user(wechat_openid) WHERE wechat_openid IS NOT NULL;

-- ==========================================
-- 2. yx_role
-- ==========================================
CREATE TABLE yx_role (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    role_key VARCHAR(64) NOT NULL UNIQUE,
    role_name VARCHAR(50) NOT NULL,
    sort_order INT DEFAULT 0,
    status SMALLINT NOT NULL DEFAULT 1,
    remark VARCHAR(500)
);

-- ==========================================
-- 3. yx_user_role
-- ==========================================
CREATE TABLE yx_user_role (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    user_id BIGINT NOT NULL REFERENCES yx_user(id),
    role_id BIGINT NOT NULL REFERENCES yx_role(id),
    UNIQUE(user_id, role_id)
);

-- ==========================================
-- 4. yx_menu
-- ==========================================
CREATE TABLE yx_menu (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    parent_id BIGINT NOT NULL DEFAULT 0,
    menu_name VARCHAR(100) NOT NULL,
    menu_type CHAR(1) NOT NULL,
    path VARCHAR(255),
    component VARCHAR(255),
    permission VARCHAR(200),
    icon VARCHAR(100),
    sort_order INT DEFAULT 0,
    visible BOOLEAN NOT NULL DEFAULT TRUE,
    status SMALLINT NOT NULL DEFAULT 1,
    remark VARCHAR(500)
);

-- ==========================================
-- 5. yx_role_menu
-- ==========================================
CREATE TABLE yx_role_menu (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    role_id BIGINT NOT NULL REFERENCES yx_role(id),
    menu_id BIGINT NOT NULL REFERENCES yx_menu(id),
    UNIQUE(role_id, menu_id)
);

-- ==========================================
-- 6. yx_conversation
-- ==========================================
CREATE TABLE yx_conversation (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    user_id BIGINT NOT NULL REFERENCES yx_user(id),
    title VARCHAR(200),
    status SMALLINT NOT NULL DEFAULT 1,
    teacher_id BIGINT REFERENCES yx_user(id),
    teacher_joined_at TIMESTAMP WITH TIME ZONE,
    last_message_at TIMESTAMP WITH TIME ZONE,
    message_count INT NOT NULL DEFAULT 0
);

CREATE INDEX idx_yx_conversation_user_status ON yx_conversation(user_id, status);
CREATE INDEX idx_yx_conversation_teacher_id ON yx_conversation(teacher_id);
CREATE INDEX idx_yx_conversation_last_message_at ON yx_conversation(last_message_at DESC);

-- ==========================================
-- 7. yx_message
-- ==========================================
CREATE TABLE yx_message (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    conversation_id BIGINT NOT NULL REFERENCES yx_conversation(id),
    sender_type SMALLINT NOT NULL,
    sender_id BIGINT,
    content TEXT NOT NULL,
    message_type SMALLINT NOT NULL DEFAULT 1,
    parent_message_id BIGINT,
    ai_confidence DECIMAL(5,4),
    ai_source_entry_ids VARCHAR(500),
    ai_source_link_ids VARCHAR(500)
);

CREATE INDEX idx_yx_message_conversation_created ON yx_message(conversation_id, created_at);

-- ==========================================
-- 8. yx_escalation
-- ==========================================
CREATE TABLE yx_escalation (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    conversation_id BIGINT NOT NULL REFERENCES yx_conversation(id),
    message_id BIGINT NOT NULL REFERENCES yx_message(id),
    student_id BIGINT NOT NULL REFERENCES yx_user(id),
    teacher_id BIGINT REFERENCES yx_user(id),
    question_summary VARCHAR(500),
    status SMALLINT NOT NULL DEFAULT 0,
    priority SMALLINT NOT NULL DEFAULT 1,
    trigger_type SMALLINT NOT NULL DEFAULT 1,
    teacher_reply TEXT,
    resolved_at TIMESTAMP WITH TIME ZONE,
    knowledge_entry_id BIGINT,
    remark VARCHAR(500)
);

CREATE INDEX idx_yx_escalation_teacher_status ON yx_escalation(teacher_id, status);
CREATE INDEX idx_yx_escalation_student_id ON yx_escalation(student_id);
CREATE INDEX idx_yx_escalation_status_priority ON yx_escalation(status, priority);

-- ==========================================
-- 9. yx_knowledge_category
-- ==========================================
CREATE TABLE yx_knowledge_category (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    parent_id BIGINT NOT NULL DEFAULT 0,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(50) NOT NULL UNIQUE,
    sort_order INT DEFAULT 0,
    description VARCHAR(500),
    icon VARCHAR(100),
    status SMALLINT NOT NULL DEFAULT 1
);

-- ==========================================
-- 10. yx_knowledge_source (必须在 entry 之前)
-- ==========================================
CREATE TABLE yx_knowledge_source (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(512),
    file_url VARCHAR(512),
    file_type VARCHAR(20),
    file_size BIGINT,
    description VARCHAR(500),
    uploader_id BIGINT REFERENCES yx_user(id)
);

-- ==========================================
-- 11. yx_knowledge_entry
-- ==========================================
CREATE TABLE yx_knowledge_entry (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    category_id BIGINT NOT NULL REFERENCES yx_knowledge_category(id),
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    summary VARCHAR(500),
    status SMALLINT NOT NULL DEFAULT 0,
    version INT NOT NULL DEFAULT 1,
    source_id BIGINT REFERENCES yx_knowledge_source(id),
    author_id BIGINT NOT NULL REFERENCES yx_user(id),
    published_at TIMESTAMP WITH TIME ZONE,
    expired_at TIMESTAMP WITH TIME ZONE,
    view_count INT NOT NULL DEFAULT 0,
    hit_count INT NOT NULL DEFAULT 0,
    remark VARCHAR(500)
);

CREATE INDEX idx_yx_knowledge_entry_cat_status ON yx_knowledge_entry(category_id, status);
CREATE INDEX idx_yx_knowledge_entry_status_pub ON yx_knowledge_entry(status, published_at DESC);
CREATE INDEX idx_yx_knowledge_entry_author_id ON yx_knowledge_entry(author_id);

-- ==========================================
-- 12. yx_knowledge_review
-- ==========================================
CREATE TABLE yx_knowledge_review (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    entry_id BIGINT NOT NULL REFERENCES yx_knowledge_entry(id),
    reviewer_id BIGINT NOT NULL REFERENCES yx_user(id),
    action SMALLINT NOT NULL,
    opinion TEXT,
    entry_version INT NOT NULL
);

-- ==========================================
-- 13. yx_knowledge_tag
-- ==========================================
CREATE TABLE yx_knowledge_tag (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    name VARCHAR(50) NOT NULL UNIQUE,
    sort_order INT DEFAULT 0
);

-- ==========================================
-- 14. yx_knowledge_entry_tag
-- ==========================================
CREATE TABLE yx_knowledge_entry_tag (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    entry_id BIGINT NOT NULL REFERENCES yx_knowledge_entry(id),
    tag_id BIGINT NOT NULL REFERENCES yx_knowledge_tag(id),
    UNIQUE(entry_id, tag_id)
);

-- ==========================================
-- 15. yx_classroom
-- ==========================================
CREATE TABLE yx_classroom (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    building VARCHAR(100) NOT NULL,
    room_number VARCHAR(50) NOT NULL,
    capacity INT,
    equipment VARCHAR(500),
    location VARCHAR(200),
    status SMALLINT NOT NULL DEFAULT 1,
    remark VARCHAR(500),
    UNIQUE(building, room_number)
);

-- ==========================================
-- 16. yx_classroom_application
-- ==========================================
CREATE TABLE yx_classroom_application (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    applicant_id BIGINT NOT NULL REFERENCES yx_user(id),
    classroom_id BIGINT NOT NULL REFERENCES yx_classroom(id),
    apply_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    purpose VARCHAR(500) NOT NULL,
    attendee_count INT,
    contact_phone VARCHAR(20),
    attachments VARCHAR(1000),
    status SMALLINT NOT NULL DEFAULT 0,
    remark VARCHAR(500)
);

CREATE INDEX idx_yx_classroom_app_applicant ON yx_classroom_application(applicant_id, status);
CREATE INDEX idx_yx_classroom_app_classroom_date ON yx_classroom_application(classroom_id, apply_date);
CREATE INDEX idx_yx_classroom_app_status ON yx_classroom_application(status);

-- ==========================================
-- 17. yx_application_review
-- ==========================================
CREATE TABLE yx_application_review (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    application_id BIGINT NOT NULL REFERENCES yx_classroom_application(id),
    reviewer_id BIGINT NOT NULL REFERENCES yx_user(id),
    action SMALLINT NOT NULL,
    opinion VARCHAR(500)
);

-- ==========================================
-- 18. yx_quick_link
-- ==========================================
CREATE TABLE yx_quick_link (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    name VARCHAR(100) NOT NULL,
    url VARCHAR(512) NOT NULL,
    description VARCHAR(500),
    category VARCHAR(50),
    tags VARCHAR(500),
    icon VARCHAR(100),
    sort_order INT DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    click_count INT NOT NULL DEFAULT 0
);

-- ==========================================
-- 19. yx_push_task (需要提前建立)
-- ==========================================
CREATE TABLE yx_push_task (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    target_type SMALLINT NOT NULL,
    target_filter TEXT,
    status SMALLINT NOT NULL DEFAULT 0,
    sender_id BIGINT NOT NULL REFERENCES yx_user(id),
    sent_at TIMESTAMP WITH TIME ZONE,
    recipient_count INT NOT NULL DEFAULT 0,
    read_count INT NOT NULL DEFAULT 0
);

-- ==========================================
-- 20. yx_notification
-- ==========================================
CREATE TABLE yx_notification (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    user_id BIGINT NOT NULL REFERENCES yx_user(id),
    title VARCHAR(200) NOT NULL,
    content TEXT,
    type SMALLINT NOT NULL,
    biz_type VARCHAR(50),
    biz_id BIGINT,
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    read_at TIMESTAMP WITH TIME ZONE,
    sender_id BIGINT,
    push_task_id BIGINT REFERENCES yx_push_task(id)
);

CREATE INDEX idx_yx_notification_user_read ON yx_notification(user_id, is_read, created_at DESC);

-- ==========================================
-- 21. yx_ai_persona
-- ==========================================
CREATE TABLE yx_ai_persona (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    teacher_id BIGINT REFERENCES yx_user(id),
    name VARCHAR(50) NOT NULL DEFAULT '小管',
    avatar_url VARCHAR(512),
    greeting TEXT,
    system_prompt TEXT,
    tone_style VARCHAR(50),
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    status SMALLINT NOT NULL DEFAULT 1
);

-- ==========================================
-- 22. yx_audit_log
-- ==========================================
CREATE TABLE yx_audit_log (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    user_id BIGINT,
    username VARCHAR(64),
    module VARCHAR(50) NOT NULL,
    action VARCHAR(50) NOT NULL,
    target_type VARCHAR(50),
    target_id BIGINT,
    description VARCHAR(500),
    request_method VARCHAR(10),
    request_url VARCHAR(500),
    request_ip VARCHAR(128),
    request_params TEXT,
    response_code INT,
    cost_time BIGINT,
    status SMALLINT NOT NULL,
    error_msg TEXT
);

CREATE INDEX idx_yx_audit_log_user ON yx_audit_log(user_id, created_at DESC);
CREATE INDEX idx_yx_audit_log_module_action ON yx_audit_log(module, action);
CREATE INDEX idx_yx_audit_log_created ON yx_audit_log(created_at DESC);

-- 外键修改：确保前面漏掉的外键处理
ALTER TABLE yx_escalation ADD CONSTRAINT fk_yx_escalation_entry FOREIGN KEY (knowledge_entry_id) REFERENCES yx_knowledge_entry(id);
