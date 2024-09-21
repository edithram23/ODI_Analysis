
SELECT
  COUNT(DISTINCT matchdate) AS matches_played
FROM ODI
WHERE
  batsman = 'KL Rahul';

SELECT
  SUM(runs) AS total_runs
FROM ODI
WHERE
  batsman = 'KL Rahul';

SELECT 
  AVG(runs) AS "Average Runs"
FROM ODI
WHERE
  batsman = 'KL Rahul';

SELECT
  COUNT(*) AS "Number of Fifties"
FROM ODI
WHERE
  batsman = "KL Rahul" AND runs BETWEEN 50 AND 99;

SELECT
  COUNT(*) AS Centuries
FROM ODI
WHERE
  batsman = "KL Rahul" AND runs >= 100;

SELECT
  SUM(fours)
FROM ODI
WHERE
  batsman = "KL Rahul";

SELECT
  SUM(sixes) AS total_sixes
FROM ODI
WHERE
  batsman = "KL Rahul";
