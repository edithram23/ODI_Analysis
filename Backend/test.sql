
SELECT
  SUM(ODI.runs)
FROM ODI
WHERE
  ODI.batsman = 'Kumar Dharmasena' AND ODI.opponent_team = 'Australia';

SELECT
  SUM(runs)
FROM ODI
WHERE
  batsman = 'Kumar Sangakkara' AND opponent_team = 'Australia';

SELECT
  SUM(runs) AS total_runs
FROM ODI
WHERE
  batsman = 'Praveen Kumar' AND opponent_team = 'Australia';

SELECT
  SUM(runs) AS total_runs
FROM ODI
WHERE
  batsman = "Vinay Kumar" AND opponent_team = "Australia";

SELECT
  SUM(runs) AS total_runs_scored
FROM ODI
WHERE
  bowler = "Bhuvneshwar Kumar" AND opponent_team = "Australia";

SELECT
  SUM(ODI.runs) AS total_runs_scored
FROM ODI
WHERE
  ODI.batsman = "Nitish Kumar" AND ODI.opponent_team = "Australia";

SELECT
  SUM(runs) AS total_runs
FROM ODI
WHERE
  batsman = 'Mukesh Kumar' AND opponent_team = 'Australia';

SELECT
  SUM(runs) AS total_runs
FROM ODI
WHERE
  batsman = "Suraj Kumar" AND opponent_team = "Australia";
