# 03_analysis.R -- main estimation and table export (demo stub)
# Fictional project for bootcamp training. This stub documents the
# table-to-code mapping that grounding checks rely on; it does not run.
#
# Inputs:  data/analysis/panel_school_month.rds   (not included in demo)
# Outputs: outputs/tab1_summary.tex   (baseline balance, 2021)
#          outputs/tab2_main.tex      (DiD estimates, 3 specs; col 2 preferred)
#          outputs/tab3_het.tex       (heterogeneity: sex, urban/rural)
#
# Specification (col 2, preferred):
#   attendance_sm ~ fsmp_d * post_m + controls + school FE + month FE,
#   SEs clustered at district level (92 clusters).
#
# est_main   <- feols(attend ~ fsmp:post + enroll + ptr + assets |
#                     school + month, cluster = ~district, data = panel)
# ... table export via modelsummary -> outputs/*.tex
