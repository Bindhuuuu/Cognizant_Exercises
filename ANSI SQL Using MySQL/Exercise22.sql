SELECT
    u.full_name,
    e.title AS event_name,
    COUNT(*) AS registration_count
FROM Registrations r
JOIN Users u
ON r.user_id = u.user_id
JOIN Events e
ON r.event_id = e.event_id
GROUP BY u.full_name, e.title
HAVING COUNT(*) > 1;