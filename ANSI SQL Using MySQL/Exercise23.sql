SELECT
    DATE_FORMAT(registration_date, '%Y-%m') AS registration_month,
    COUNT(registration_id) AS total_registrations
FROM Registrations
GROUP BY DATE_FORMAT(registration_date, '%Y-%m')
ORDER BY registration_month;