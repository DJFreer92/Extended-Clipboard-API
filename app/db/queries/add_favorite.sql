INSERT OR IGNORE INTO FavoriteClips (ClipID)
SELECT ID FROM Clips WHERE ID = :clip_id;
