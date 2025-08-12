-- Assumes the tag already exists (service layer ensures creation via add_tag_if_not_exists.sql)
INSERT OR IGNORE INTO ClipTags (ClipID, TagID)
SELECT :clip_id, ID FROM Tags WHERE Name = :tag_name
