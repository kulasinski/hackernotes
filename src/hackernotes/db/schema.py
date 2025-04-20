# hackernotes/db/schema.py

# Schema SQL loaded as a multiline string to be used in init_db()
SCHEMA_SQL = """

CREATE TABLE IF NOT EXISTS user (
    id TEXT PRIMARY KEY,
    name TEXT,
    email TEXT,
    settings TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS workspace (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    name TEXT NOT NULL,
    model_backend TEXT NOT NULL,
    model_config TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS note (
    id TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    title TEXT,
    archived BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workspace_id) REFERENCES workspace(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS snippet (
    id TEXT PRIMARY KEY,
    note_id TEXT NOT NULL,
    content TEXT NOT NULL,
    position INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (note_id) REFERENCES note(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tag (
    name TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS entity (
    name TEXT PRIMARY KEY,
    entity_type TEXT
);

CREATE TABLE IF NOT EXISTS time_expr (
    value TEXT PRIMARY KEY,
    literal TEXT NOT NULL,
    scope TEXT CHECK(scope IN ('century', 'year', 'month', 'week', 'day', 'hour', 'minute', 'second', 'millisecond'))
);

CREATE TABLE IF NOT EXISTS snippet_tag (
    snippet_id TEXT,
    tag_name TEXT,
    FOREIGN KEY (snippet_id) REFERENCES snippet(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_name) REFERENCES tag(name),
    PRIMARY KEY (snippet_id, tag_name)
);

CREATE TABLE IF NOT EXISTS snippet_entity (
    snippet_id TEXT,
    entity_name TEXT,
    FOREIGN KEY (snippet_id) REFERENCES snippet(id) ON DELETE CASCADE,
    FOREIGN KEY (entity_name) REFERENCES entity(name),
    PRIMARY KEY (snippet_id, entity_name)
);

CREATE TABLE IF NOT EXISTS snippet_time_expr (
    snippet_id TEXT,
    time_value TEXT,
    FOREIGN KEY (snippet_id) REFERENCES snippet(id) ON DELETE CASCADE,
    FOREIGN KEY (time_value) REFERENCES time_expr(value),
    PRIMARY KEY (snippet_id, time_value)
);

CREATE TABLE IF NOT EXISTS note_tag (
    note_id TEXT,
    tag_name TEXT,
    FOREIGN KEY (note_id) REFERENCES note(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_name) REFERENCES tag(name),
    PRIMARY KEY (note_id, tag_name)
);

CREATE TABLE IF NOT EXISTS note_entity (
    note_id TEXT,
    entity_name TEXT,
    FOREIGN KEY (note_id) REFERENCES note(id) ON DELETE CASCADE,
    FOREIGN KEY (entity_name) REFERENCES entity(name),
    PRIMARY KEY (note_id, entity_name)
);

CREATE TABLE IF NOT EXISTS note_time_expr (
    note_id TEXT,
    time_value TEXT,
    FOREIGN KEY (note_id) REFERENCES note(id) ON DELETE CASCADE,
    FOREIGN KEY (time_value) REFERENCES time_expr(value),
    PRIMARY KEY (note_id, time_value)
);

CREATE TABLE IF NOT EXISTS graph_node (
    id TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    label TEXT NOT NULL,
    parent_id TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workspace_id) REFERENCES workspace(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES graph_node(id)
);

CREATE TABLE IF NOT EXISTS note_graph_node (
    note_id TEXT,
    node_id TEXT,
    PRIMARY KEY (note_id, node_id),
    FOREIGN KEY (note_id) REFERENCES note(id) ON DELETE CASCADE,
    FOREIGN KEY (node_id) REFERENCES graph_node(id)
);

CREATE TABLE IF NOT EXISTS prompt (
    id INTEGER PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    prompt_type TEXT CHECK(prompt_type IN ('chat', 'generate', 'annotate', 'classify')),
    title TEXT,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workspace_id) REFERENCES workspace(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS automation_queue (
    id INTEGER PRIMARY KEY,
    note_id TEXT,
    snippet_id TEXT,
    model_id TEXT,
    task_type TEXT NOT NULL,
    status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'running', 'success', 'failed')),
    status_detail TEXT,
    scheduled_at DATETIME,
    executed_at DATETIME,
    result TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

"""