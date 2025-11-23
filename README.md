# LinkedIn People Profiles Dataset Transformation

This repository contains a dataset of LinkedIn people profiles and a transformation script to convert it to a simplified format.

## Files

- `archive/LinkedIn_people_profiles_datasets.csv` - Original LinkedIn profiles dataset (1000 records)
- `archive/LinkedIn_people_profiles_transformed.csv` - Transformed dataset with selected columns
- `transform_linkedin_data.py` - Python script to perform the transformation

## Transformation Details

The transformation script (`transform_linkedin_data.py`) converts the original dataset to a new format with the following columns:

### Output Columns

1. **LinkedInUserId** - Extracted from the "id" column
2. **Name** - Extracted from the "name" column  
3. **University** - Extracted from the "education" JSON field (first educational institution)
4. **Company** - Extracted from the "current_company:name" column
5. **Project** - Extracted from the "position" field (current role/title)
6. **Publication** - Left empty (not available in source data)

### How It Works

The script:
- Reads the original CSV file with 26 columns
- Parses JSON fields (education, experience) to extract relevant information
- Handles missing/null values by using empty strings
- Outputs a clean CSV with only the 6 required columns

### Running the Transformation

```bash
# Install dependencies
pip3 install pandas

# Run the transformation
python3 transform_linkedin_data.py
```

The script will:
1. Read `archive/LinkedIn_people_profiles_datasets.csv`
2. Transform the data
3. Save the output to `archive/LinkedIn_people_profiles_transformed.csv`

### Data Statistics

From the 1000 records:
- 720 (72%) have university information
- 833 (83.3%) have company information
- 986 (98.6%) have project/position information
- All records have LinkedInUserId and Name

### Example Output

```csv
LinkedInUserId,Name,University,Company,Project,Publication
catherinemcilkenny,"Catherine Fitzpatrick (McIlkenny), B.A",Queen's University Belfast,,Snr Business Analyst at Emploi et Développement social Canada (EDSC) / Employment and Social Development Canada (ESDC),
margot-bon-51a04624,Margot Bon,Xebia Academy International,Gemeente Utrecht,Communicatieadviseur Corporate & Strategie Gemeente Utrecht,
```

## Requirements

- Python 3.6+
- pandas library
