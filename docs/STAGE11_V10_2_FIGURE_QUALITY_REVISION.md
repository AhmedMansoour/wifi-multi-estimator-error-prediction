# v10.2 — Figure-quality correction and verification report

**Editorial scope:** Source-controlled figure and layout revision of EAAI v10.1. No new model fitting, experimental measurements, changes to numerical tables, or claims of fresh statistical validation.

## Author instruction: preserve Figure 3

The main-paper Figure 3 (Transformer encoder computation) and original SOD six-estimator supplementary case Figure 3 asset were kept **byte-for-byte identical**. The source hashes are supplied in the JSON manifest. The supplementary case figure may have a different ordinal after the removal of a redundant earlier supplementary image; the scientific image is unchanged.

## Verified updates

1. **Main Fig. 13 and SM walking-track companion:** Reordered the original 4-panel vector PDFs to read (a) positions, (b) observed versus forecast error, (c) signed discrepancy, and (d) absolute-discrepancy ECDF. Preserved the original plotted information and reference-position limitations. Corrected the final vector-panel label rendering and reviewed the resulting graphic at print size.
2. **Supplement duplicate:** Removed the exact duplicate of Main Fig. 12 from supplementary source. Retained the supporting S1/S4/N3 numeric examples as prose and cross-referenced the unchanged main figure.
3. **Supplement numbering:** Standardized every supplementary figure as Figure S1 through Figure S16. The historical estimator-identity ablation no longer changes to an appendix-numbered B.16.
4. **Results-page composition:** Relaxed an unnecessary figure barrier and adjusted double-column float fractions. Main Fig. 12 now shares page 25 with discussion; Main Fig. 13 shares page 26 with discussion. No reduction of plotting font sizes.
5. **Main Fig. 4:** Intensified the brightness-to-blue mapping of its six embedded hexbin-density image layers. Data positions, axes, legends, annotation values, and the 0–25 m display window remain unchanged. This is display-only density-contrast enhancement; it does not recompute counts or experimental metrics.
6. **Main Fig. 7 and Fig. 10 captions:** Made tail-calibration and descriptive shading qualifications explicit, avoiding false protection-level/decision-boundary interpretation. Numeric values unchanged.
7. **Selected SM figures:** Increased available printable width for SOD S4 and NearLink N3 six-estimator panels, decision-risk comparison, RSS-neighborhood evidence, selective-use workload, mobile calibration and WKNN walking panels. The originally approved SOD S1 six-estimator panel was left untouched.
8. **Historical figure limitation:** Supplement estimator-identity ablation caption now acknowledges the unrecovered 22-descriptor indices; it is not presented as an isolated 12-geometry-feature experiment.
9. **Layout and compilation:** Removed the minor pre-existing SM page-4 overfull vbox by adjusting float separation; full LaTeX replay with references complete. Main and anonymous PDFs each 29 pages; supplement 38 pages.

## Preservation and scope limits

- All existing table environments, including every numerical cell, are byte-for-byte identical to v10.1 in the source. Table blocks were tested for equality.
- No original real research data files, model checkpoints, or predictions were accessed or changed for this visual revision.
- Figures that require **replotting from original per-scan values** to improve inherent font sizes, contrast semantics, or label placement have not been reconstructed from approximate data; underlying original assets remain available. In particular, the SOD S1 diagram remains exactly as the author requested, and the agreement-versus-correctness graphic is source-preserved (only its caption was clarified).
- Author has explicitly authorized publication of the Block Z trajectory data; no privacy-based removal was made.

**Figure count after de-duplication:** Main = 13, Supplement = 16. **Status:** v10.2 figure-quality and numbering fixes are compiled and checked. This is not an audit of all underlying experimental calculations or EAAI submission formatting.
