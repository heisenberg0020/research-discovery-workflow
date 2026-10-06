# Fictional current-source records

These are authored definitions for this finite exercise. They are not real publications, experiments, or observations. All values below are stipulated.

## C1: source and transform

The source quantity is `x∈{15,25}`, each with probability `1/2`. Its units are the units used by the final action and loss. A report producer computes `q=(x−20)/5`, giving reports `−1` and `1`. It stores `q` and a shared transform specification containing a center of `20` and a scale of `5`. The report contains no noise, and the full specification is available to the consumer. The report does not alter `x`.

## C2: decision interface

The consumer selects a real action `a`, interpreted in original source units. Its expected objective is squared error plus report cost. The no-report comparator selects one constant `a`; the report-based comparator may choose a different `a` for each observed `q`. The fixed cost of obtaining the report is `1`, in squared-loss units. A zero-cost no-report option is available.

## C3: evidence scope

The current packet contains no measured compute savings, resource prices, training outcomes, human observations, or implementation benchmarks. Mathematical claims may be checked from these definitions. An older package, if subsequently supplied, is a distinct input rather than current-source evidence.
