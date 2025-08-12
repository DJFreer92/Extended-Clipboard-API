SELECT
	Clips.ID AS ClipID,
	Clips.Content AS Content,
	Clips.FromAppName AS FromAppName,
	GROUP_CONCAT(Tags.Name, ',') AS Tags,
	Clips.Timestamp AS Timestamp
FROM Clips
LEFT JOIN ClipTags ON Clips.ID = ClipTags.ClipID
LEFT JOIN Tags ON ClipTags.TagID = Tags.ID
GROUP BY Clips.ID, Clips.Content, Clips.FromAppName, Clips.Timestamp
ORDER BY Clips.ID DESC;
