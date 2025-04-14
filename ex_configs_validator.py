import yaml

def validate_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)

    # Validate version
    if 'version' not in config:
        raise ValueError("Missing 'version' in configuration.")

    # Validate experiment section
    experiment = config.get('experiment', {})
    required_material_keys = ['name', 'young_s', 'poisson_ratio', 'density', 'thickness']
    for key in required_material_keys:
        if key not in experiment.get('material', {}):
            raise ValueError(f"Missing '{key}' in experiment.material.")

    # Validate acquisition section
    acquisition = config.get('acquisition', {})
    if 'device' not in acquisition or 'sampling_rate' not in acquisition:
        raise ValueError("Missing 'device' or 'sampling_rate' in acquisition.")

    # Validate processing section
    processing = config.get('processing', {})
    if 'pre_filters' not in processing or 'imaging_method' not in processing:
        raise ValueError("Missing 'pre_filters' or 'imaging_method' in processing.")
    
    # Validate pre_filters
    pre_filters = processing.get('pre_filters', [])
    for filter_item in pre_filters:
        if 'type' not in filter_item:
            raise ValueError("Each pre_filter must have a 'type'.")
        if filter_item['type'] == 'bandpass_filter':
            if 'low_cutoff' not in filter_item or 'high_cutoff' not in filter_item:
                raise ValueError("Bandpass filter must have 'low_cutoff' and 'high_cutoff'.")

    print("Configuration is valid.")

# Example usage
if __name__ == "__main__":
    validate_config("f:\\ANW\\Lab-framework-core\\ex_configs.yaml")
