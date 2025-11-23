#!/usr/bin/env python3
"""
Transform LinkedIn people profiles dataset to new format.
Extracts specific columns and parses JSON fields for university and project information.
"""

import pandas as pd
import json
import sys


def extract_university(education_str):
    """
    Extract university name from education JSON field.
    Returns the first educational institution found.
    """
    if pd.isna(education_str) or education_str == 'null':
        return ''
    
    try:
        # Parse the JSON string
        education_list = json.loads(education_str)
        
        # Get the first education entry if available
        if isinstance(education_list, list) and len(education_list) > 0:
            first_edu = education_list[0]
            if isinstance(first_edu, dict) and 'title' in first_edu:
                return first_edu['title']
    except (json.JSONDecodeError, TypeError, KeyError):
        pass
    
    return ''


def extract_project(experience_str, position_str):
    """
    Extract project information from experience field or position field.
    Priority: position field (current role), then first position in experience.
    """
    # First, try to use the position field (current position)
    if pd.notna(position_str) and position_str != 'null':
        return position_str
    
    # If position is empty, try to extract from experience
    if pd.isna(experience_str) or experience_str == 'null':
        return ''
    
    try:
        # Parse the JSON string
        experience_list = json.loads(experience_str)
        
        # Get the first experience entry if available
        if isinstance(experience_list, list) and len(experience_list) > 0:
            first_exp = experience_list[0]
            if isinstance(first_exp, dict):
                # Try to get the first position's title
                if 'positions' in first_exp and isinstance(first_exp['positions'], list):
                    if len(first_exp['positions']) > 0:
                        first_position = first_exp['positions'][0]
                        if isinstance(first_position, dict) and 'title' in first_position:
                            title = first_position['title']
                            company = first_exp.get('company', '')
                            if company:
                                return f"{title} at {company}"
                            return title
    except (json.JSONDecodeError, TypeError, KeyError):
        pass
    
    return ''


def transform_linkedin_data(input_file, output_file):
    """
    Transform LinkedIn profiles CSV to new format.
    
    Args:
        input_file: Path to input CSV file
        output_file: Path to output CSV file
    """
    print(f"Reading data from {input_file}...")
    
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    print(f"Loaded {len(df)} rows")
    print(f"Original columns: {df.columns.tolist()}")
    
    # Create new dataframe with required columns
    print("\nTransforming data...")
    
    transformed_df = pd.DataFrame({
        'LinkedInUserId': df['id'].fillna(''),
        'Name': df['name'].fillna(''),
        'University': df['education'].apply(extract_university),
        'Company': df['current_company:name'].fillna(''),
        'Project': df.apply(lambda row: extract_project(row['experience'], row['position']), axis=1),
        'Publication': ''  # Empty as not available in the dataset
    })
    
    print(f"\nTransformed columns: {transformed_df.columns.tolist()}")
    print(f"Sample rows:")
    print(transformed_df.head(3).to_string())
    
    # Save to CSV
    print(f"\nSaving transformed data to {output_file}...")
    transformed_df.to_csv(output_file, index=False)
    
    print(f"Done! Saved {len(transformed_df)} rows to {output_file}")


if __name__ == '__main__':
    input_file = 'archive/LinkedIn_people_profiles_datasets.csv'
    output_file = 'archive/LinkedIn_people_profiles_transformed.csv'
    
    try:
        transform_linkedin_data(input_file, output_file)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
