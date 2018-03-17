


-- number of unique users
SELECT COUNT(*)
FROM
( SELECT uid FROM nodes
UNION
SELECT uid FROM ways);


-- number of nodes
SELECT COUNT(id)
FROM nodes;

-- number of ways
SELECT COUNT(id) FROM ways;



-- confirm only nodes belonging to Cologne were imported
SELECT tags.value, COUNT(*) as count
FROM (SELECT * FROM nodes_tags UNION ALL 
      SELECT * FROM ways_tags) tags
WHERE tags.key = 'city'
GROUP BY tags.value
ORDER BY count DESC;



-- DELETE FROM nodes_tags WHERE key = 'city' and value != 'Köln';
-- DELETE FROM ways_tags WHERE key = 'city' and value != 'Köln';  


-- View phones that do not match pattern
SELECT tags.value, tags.id
FROM (SELECT * FROM nodes_tags UNION 
      SELECT * FROM ways_tags) tags
WHERE tags.key = 'phone' and tags.value NOT LIKE '+49 ___ %';

-- Inspect element with 'dirty' phone number
SELECT *
FROM nodes_tags
WHERE id = 1788497081;




-- find most common restaurant type
SELECT a.value, b.value
FROM nodes_tags a
JOIN (SELECT id, value FROM nodes_tags WHERE key = 'amenity') b
ON a.id = b.id
WHERE key = 'cuisine';

-- check if there are cuisine values in the ways table
SELECT count(*)
FROM ways_tags
WHERE key = 'cuisine';


-- find most common fast food type
SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags 
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='restaurant') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='cuisine'
GROUP BY nodes_tags.value
ORDER BY num DESC; 

--  Most popular drug store
SELECT a.value, COUNT(a.id) as count
FROM nodes_tags a
JOIN (SELECT id FROM nodes_tags WHERE value = 'chemist') b
ON a.id = b.id
WHERE a.key = 'name'
GROUP BY a.value
ORDER BY count DESC;


-- Places of worship grouped by religion
SELECT ways_tags.value, COUNT(*) as num
FROM ways_tags
    JOIN (SELECT DISTINCT(id) FROM ways_tags WHERE value='place_of_worship') a
    ON ways_tags.id=a.id
WHERE ways_tags.key='religion'
GROUP BY ways_tags.value
ORDER BY num DESC;

-- Christian denominations
SELECT b.value, COUNT(*) as num
FROM ways_tags
JOIN (SELECT DISTINCT(id) FROM ways_tags WHERE value='place_of_worship') a
ON ways_tags.id=a.id
JOIN (SELECT DISTINCT(id), value FROM ways_tags WHERE key = 'denomination') b
ON a.id = b.id 
WHERE ways_tags.key='religion' AND ways_tags.value = 'christian'
GROUP BY b.value
ORDER BY num DESC
LIMIT 10;

--- Select top 10 users
SELECT a.user, COUNT(*) as num
FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) a
GROUP BY a.user
ORDER BY num DESC
LIMIT 10;

