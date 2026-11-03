# Clean baseline and endline household data
library(dplyr)
root <- here::here()
bl <- read.csv(file.path(root, "data", "raw", "baseline_hh.csv"))
el <- read.csv(file.path(root, "data", "raw", "endline_hh.csv"))

bl <- bl %>%
  mutate(log_cons = log(consumption_pc),
         large_hh = as.integer(hh_size >= 7))

hh <- left_join(bl, el, by = "hhid")
dir.create(file.path(root, "data", "clean"), showWarnings = FALSE, recursive = TRUE)
saveRDS(hh, file.path(root, "data", "clean", "hh_panel.rds"))
