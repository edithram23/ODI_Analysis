
SELECT
  COUNT(*) AS MatchesPlayed
FROM ODI
WHERE
  batsman = "Kapil Dev";

SELECT SUM(runs)
FROM ODI
WHERE batsman = 'Kapil Dev';

SELECT AVG(runs) AS "Run Average"
FROM ODI
WHERE batsman = 'Kapil Dev';

SELECT
  COUNT(*) AS fifties
FROM ODI
WHERE
  batsman = 'Kapil Dev' AND runs >= 50 AND runs < 100;

SELECT
  COUNT(*) AS Number_of_Centuries
FROM ODI
WHERE
  batsman = 'Kapil Dev' AND runs >= 100;

SELECT
  SUM(fours) AS total_fours
FROM ODI
WHERE
  batsman = 'Kapil Dev';

SELECT
  SUM(sixes)
FROM ODI
WHERE
  batsman = 'Kapil Dev';
