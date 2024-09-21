
SELECT
  COUNT(*) AS matches_played
FROM ODI
WHERE
  batsman = "Joe Root";

SELECT
  SUM(runs) AS total_runs
FROM ODI
WHERE
  batsman = 'Joe Root';

SELECT 
  AVG(runs) AS run_average
FROM ODI
WHERE
  batsman = 'Joe Root';

SELECT
  COUNT(*) AS "Number of Fifties"
FROM ODI
WHERE
  batsman = 'Joe Root' AND runs >= 50;

SELECT
  COUNT(*) AS centuries
FROM ODI
WHERE
  batsman = 'Joe Root' AND runs >= 100;

SELECT
  SUM(fours)
FROM ODI
WHERE
  batsman = "Joe Root";

SELECT
  SUM(sixes) AS total_sixes
FROM ODI
WHERE
  batsman = 'Joe Root';
