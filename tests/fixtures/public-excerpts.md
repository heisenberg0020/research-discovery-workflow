# Fictional primary-source excerpts — not real papers

These are synthetic fixtures. Identifiers below are local anchors, not external citations.

## Fixture P: fixed combination of two estimators

Setup: each product receives forecasts f_recent and f_long using recent and long-window demand counts. A single mixing coefficient w is selected on development data, then output f=w*f_recent+(1-w)*f_long for all decisions. Observed demand is the learning target. The report gives no subgroup table or study of abrupt changes. It reports an aggregate error improvement over either estimator in its own synthetic setting, but no comparison with adaptive mixtures or guarantees under drift. No resource-cost study was done.

## Fixture Q: known conditional mixture

Setup: a context feature c is observable before the demand decision. Two fixed estimators are mixed with a learned logistic weight g(c), trained using out-of-fold predictions and squared error. Low-support contexts shrink toward a global weight. At inference only c and the two predictions are used. The fixture reports aggregate and predeclared subgroup errors under stable context definitions. It does not test missing or delayed features and does not establish that conditional weights are optimal for every decision objective. This is an existing method in the fictional corpus, not a novel operation to claim.

## Fixture R: practitioner operational note

The warehouse can obtain an additional pre-decision sensor reading at a per-query cost. Some readings arrive after the stock action and are then unusable for that action. Reported sensor availability differs by shift because of maintenance. The note states that forecast error and actual shortage/holding costs are distinct quantities; the same forecast may lead to different actions under asymmetric costs. No rates, effect sizes, optimal policy or causal result are supplied. These observations identify possible questions, not evidence that a specific new method works.
