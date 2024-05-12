a = """
SELECT "qq"->'Values' From
(SELECT ("TX"->>0)::jsonb AS qq
FROM public."dataStoring_jsonshort");
"""

b = """
SELECT (("TX"->>0)::jsonb->'Name')::varchar(50) AS "Name",
	(("TX"->>0)::jsonb->'status')::varchar(50) AS "Value", "date"
FROM public."dataStoring_jsonshort" ORDER by "date" DESC limit 5;
"""
c = """
SELECT 
    UNIX_TIMESTAMP(<time_column>) as time_sec, 
    <value column> as value, 
    <series name column> as metric 
FROM <table name> 
WHERE $__timeFilter(time_column)
ORDER BY <time_column> ASC;
"""

d = """
SELECT 
	"sensor"->>'ID' AS "ID",
	"sensor"->>'Name' AS "Name", 
	"sensor"->>'status' AS "status",
	"sensor"->>'Values' AS "Values",
	CASE
    WHEN "sensor"->>'status' = 'Connected' THEN 1
    WHEN "sensor"->>'status' = 'Disconnected' THEN 0
    ELSE NULL
  END AS "status",
	"time"
FROM(
SELECT ("TX"->>index)::jsonb AS "sensor", "date" AS "time"
FROM (
    SELECT *
    FROM public."dataStoring_jsonshort"
    ORDER BY "date" DESC
    LIMIT 1000
) AS subquery, 
LATERAL generate_series(0, 6) AS index
ORDER BY "date" DESC
LIMIT 7000)
ORDER BY "time" ASC;


"""