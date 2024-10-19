
SELECT
  team,
  SUM(runs) AS total_runs
FROM ODI
GROUP BY
  team
ORDER BY
  total_runs DESC;
