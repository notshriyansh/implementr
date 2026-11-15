ALTER TABLE workspaces
ADD COLUMN IF NOT EXISTS selected_repository_id TEXT NULL;