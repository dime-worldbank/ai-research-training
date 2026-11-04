# Main script: runs the full Cash Plus pipeline in order
# Set the project root before running
root <- here::here()
source(file.path(root, "code", "01_clean.R"))
source(file.path(root, "code", "02_balance.R"))
source(file.path(root, "code", "03_analysis.R"))
