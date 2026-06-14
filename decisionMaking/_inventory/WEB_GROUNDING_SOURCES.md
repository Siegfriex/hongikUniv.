# DecisionMaking Enhanced RAG Web Grounding Sources

PDF transcript anchors remain the primary evidence. These web sources are supplemental grounding for solver vocabulary, spreadsheet functions, and standard optimization formulations.

| web_id | title | use | url |
|---|---|---|---|
| `WEB_OR_TOOLS_LP` | Google OR-Tools: Solving an LP Problem | LP/Simplex-style solver model grounding: variables, constraints, objective, optimal solution. | https://developers.google.com/optimization/lp/lp_example |
| `WEB_OR_TOOLS_MIP` | Google OR-Tools: Solving a MIP Problem | Integer and mixed-integer model grounding: integer variables, constraints, objective, MIP solver. | https://developers.google.com/optimization/mip/mip_example |
| `WEB_OR_TOOLS_ASSIGNMENT` | Google OR-Tools: Solving an Assignment Problem | Assignment constraints: each worker at most one task and each task exactly one worker. | https://developers.google.com/optimization/assignment/assignment_example |
| `WEB_OR_TOOLS_MIN_COST_FLOW` | Google OR-Tools: Minimum Cost Flows | Min-cost flow grounding: start nodes, end nodes, capacities, unit costs, supplies/demands. | https://developers.google.com/optimization/flow/mincostflow |
| `WEB_OR_TOOLS_MAX_FLOW` | Google OR-Tools: Maximum Flows | Maximum-flow grounding: nodes/arcs, capacities, source, sink, flow conservation. | https://developers.google.com/optimization/flow/maxflow |
| `WEB_MS_SUMPRODUCT` | Microsoft Support: SUMPRODUCT function | Spreadsheet objective grounding: multiply corresponding arrays and sum the products. | https://support.microsoft.com/en-US/Excel/sumproduct-function |
| `WEB_MS_SUMIF` | Microsoft Support: SUMIF function | Spreadsheet node-balance grounding: sum rows that satisfy a node criterion. | https://support.microsoft.com/en-US/Excel/sumif-function |
| `WEB_MS_SOLVERADD` | Microsoft Learn: SolverAdd Function | Excel Solver constraint grounding: adding relational constraints to a solver model. | https://learn.microsoft.com/en-us/office/vba/excel/concepts/functions/solveradd-function |
| `WEB_MS_SOLVERSOLVE` | Microsoft Learn: SolverSolve Function | Excel Solver execution grounding: solving the configured model. | https://learn.microsoft.com/en-us/office/vba/excel/concepts/functions/solversolve-function |
