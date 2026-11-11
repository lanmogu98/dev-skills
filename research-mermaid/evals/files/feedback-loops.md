# Design optimization and predictor calibration

Synthetic continuing research process with two mutable objects: a candidate design and a performance predictor. A fixed feasibility specification constrains proposed designs.

A design proposer uses the current predictor's estimates plus measured performance of previous designs to choose the next candidate. A physical evaluator measures the candidate and appends the design/measurement pair to a persistent archive. The predictor estimate used at proposal time is retained with that design and its measured result; an audit uses this recorded estimate, not a new prediction from a later model. The measured result feeds subsequent design proposals.

When a calibration audit detects unacceptable prediction error on new measurements, a calibrator uses the archive to update the predictor. That updated predictor supplies estimates for subsequent design proposals. The predictor's error is evaluated using the archived predictions paired with measured results; measured performance itself is not the prediction error.

Calibration is event-driven and is not required after every design trial. Design trials generate observations for calibration; calibration changes the estimates used for future design trials. Neither loop has a specified terminal condition, strict nesting, execution frequency, or synchronization barrier. The source does not supply a measured improvement or convergence claim.
