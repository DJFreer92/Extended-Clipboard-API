SELECT
	Clips.ID AS ClipID,
	Clips.Content AS Content,
	Clips.FromAppName AS FromAppName,
	GROUP_CONCAT(Tags.Name, ',') AS Tags,
	Clips.Timestamp AS Timestamp,
	CASE WHEN FavoriteClips.ClipID IS NOT NULL THEN 1 ELSE 0 END AS IsFavorite
FROM Clips
LEFT JOIN FavoriteClips ON Clips.ID = FavoriteClips.ClipID
LEFT JOIN ClipTags ON Clips.ID = ClipTags.ClipID
LEFT JOIN Tags ON ClipTags.TagID = Tags.ID
WHERE Clips.ID < :before_id
GROUP BY Clips.ID, Clips.Content, Clips.FromAppName, Clips.Timestamp
ORDER BY Clips.ID DESC
LIMIT COALESCE(:n, 999999);
