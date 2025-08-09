CREATE TRIGGER IF NOT EXISTS delete_old_if_duplicate
BEFORE INSERT ON Clips
BEGIN
	DELETE FROM Clips
	WHERE Content = NEW.Content;
END;
