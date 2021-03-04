# tidy-models

Some boilerplate classes and utility funcitons for keeping model results tidy.

## Modules
* `model_identifier`
* `databases`
* `utils`
* `multicuda`

## Notes
`ModelIdentifier` assumes models are stored in directories.

## Examples

### Save some fake training results.
```
import tidy_models as tm
import tidy_models.databases.pandas.core as db

fp_db_fit = 'path/to/db_fit.txt`

# Define a simple model identifier.
mid = tm.ModelIdentifier(
    arch_id=0, input_id=0, hypers={'n_dim': 2}, split=0
)

# Create some fake results.
assoc_data = {
    'n_epoch': 111,
    'train_time_s': 88,
    'loss': 1.234,
    'loss_val': 1.345,
}

# Update fit database.
if not fp_db_fit.exists():
    db.create_empty_db(
        fp_db_fit,
        columns=['arch_id', 'input_id', 'split_seed', 'n_split', 'split']
    )
df_fit_log = db.load_db(fp_db_fit)
df_fit_log = db.update_one(df_fit_log, mid.as_dict(), assoc_data)
db.save_db(df_fit_log, fp_db_fit)
```

### Select best-performing hyperparameters
```
import tidy_models as tm
import tidy_models.databases.pandas.core as db

# Load fit database.
fp_db_fit = 'path/to/db_fit.txt`
df_fit = db.load_db(fp_db_fit)

# Collapse results across different CV splits.
id_data = {'arch_id': 0, 'input_id': 0}
df_fit_collapse = tm.utils.collapse_splits(df_fit, id_data)

# Select best hyperparameters according to `monitor_key`.
monitor_key = 'loss_val'
df_fit_best = tm.utils.select_hypers(
    df_fit_collapse, id_data, monitor_key
)
```