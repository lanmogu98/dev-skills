# Assay workflow with supporting information

Synthetic laboratory protocol for estimating analyte concentration from prepared specimens.

The main specimen path is: received specimen → preparation → instrument acquisition → concentration estimation → result report. A preparation SOP constrains preparation; the acquired signal is the input to estimation.

Background literature informs the analyst's choice of estimation model. It is contextual support, not specimen material or an operation executed for each specimen. The selected model is an explicit input to concentration estimation.

Before the specimen batch, measurements of a known reference are used to fit calibration coefficients. Those coefficients are required inputs to concentration estimation. A quality-control reference is also measured during acquisition. Its observed drift is sent to the calibration procedure; unacceptable drift triggers recalibration for subsequent estimates. The source does not specify retroactive correction of earlier reports, batch reprocessing, or an automatic rejection branch.

Keep the preparation constraint, model-selection dependency, calibration-coefficient input, and drift feedback distinct. No allocation, blinding, randomization, replicate count, uncertainty formula, or statistical result is supplied.
