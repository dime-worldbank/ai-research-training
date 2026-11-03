# Main ITT estimates, standard errors clustered by village
library(dplyr)
library(fixest)
root <- here::here()
hh <- readRDS(file.path(root, "data", "clean", "hh_panel.rds"))

m1 <- feols(log(consumption_pc_el) ~ treatment + log_cons, cluster = ~village_id, data = hh)
m2 <- feols(food_insecure_el ~ treatment + food_insecure, cluster = ~village_id, data = hh)
m3 <- feols(child_haz_el ~ treatment, cluster = ~village_id, data = hh)
etable(m1, m2, m3, file = file.path(root, "output", "itt_table.tex"))
