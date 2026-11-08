-- name: users
-- 1. Список владельцев, SELECT.
SELECT * FROM users ORDER BY username;
-- name: sources
-- 2. Список источников, SELECT DISTINCT; NULL показывается отдельно.
SELECT DISTINCT source FROM clicks ORDER BY source;
-- name: available
-- 3. WHERE: доступные на выбранную дату ссылки; отключённые исключены.
SELECT code FROM links
WHERE is_active = 1 AND created_at <= :date AND expires_at > :date
ORDER BY code;
-- name: search
-- 4. WHERE: поиск по коду или адресу.
SELECT code FROM links WHERE code LIKE :query OR url LIKE :query
ORDER BY code;
-- name: links
-- 5. JOIN: ссылки с владельцами, включая ссылки без переходов.
SELECT l.*, u.username, u.email, u.registered_at, COUNT(c.id) AS clicks_count
FROM links l JOIN users u ON u.id = l.owner_id
LEFT JOIN clicks c ON c.code = l.code
GROUP BY l.code ORDER BY l.created_at, l.code;
-- name: clicks
-- 6. JOIN трёх таблиц: переход, ссылка и владелец.
SELECT c.id FROM clicks c JOIN links l ON l.code = c.code
JOIN users u ON u.id = l.owner_id ORDER BY c.clicked_at, c.id;
-- name: totals
-- 7. Агрегат: суммарное количество ссылок и активных флагов.
SELECT COUNT(*) AS total, COALESCE(SUM(is_active),0) AS active FROM links;
-- name: click_totals
-- 8. Агрегаты: число переходов, первая и последняя даты.
SELECT COUNT(*) AS total, MIN(clicked_at) AS first_date,
MAX(clicked_at) AS last_date FROM clicks;
-- name: by_link
-- 9. GROUP BY + LEFT JOIN сохраняет ссылки с нулём переходов.
SELECT l.code AS label, COUNT(c.id) AS total FROM links l
LEFT JOIN clicks c ON c.code = l.code
GROUP BY l.code ORDER BY total DESC, l.code;
-- name: by_source
-- 10. GROUP BY по источнику.
SELECT COALESCE(source,'не указан') AS label, COUNT(*) AS total FROM clicks
GROUP BY source ORDER BY total DESC, label;
-- name: popular
-- 11. HAVING фильтрует группы после подсчёта.
SELECT code AS label, COUNT(*) AS total FROM clicks
GROUP BY code HAVING COUNT(*) >= :minimum ORDER BY total DESC, code;
-- name: recent
-- 12. Стабильная сортировка, LIMIT и OFFSET.
SELECT id FROM clicks ORDER BY clicked_at DESC, id DESC
LIMIT :limit OFFSET :offset;
-- name: by_owner
-- 13. GROUP BY: количество ссылок каждого владельца.
SELECT u.username AS label, COUNT(l.code) AS total FROM users u
LEFT JOIN links l ON l.owner_id=u.id GROUP BY u.id ORDER BY u.username;
-- name: click_objects
-- 14. Исходные данные переходов для восстановления объектной модели.
SELECT * FROM clicks ORDER BY id;
