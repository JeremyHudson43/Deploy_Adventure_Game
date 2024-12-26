import os

def log(message):
    print(f"[LOG] {message}")

def process_files_in_dirs(root_dir, target_dirs, extensions, output_file):
    log(f"Processing files in target directories: {target_dirs}")
    log(f"Target extensions: {extensions}")
    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for target_dir in target_dirs:
                target_path = os.path.join(root_dir, target_dir)
                if not os.path.exists(target_path):
                    log(f"Directory does not exist: {target_path}")
                    continue
                
                for root, _, files in os.walk(target_path):
                    log(f"Entering directory: {root}")
                    for file in files:
                        if any(file.endswith(ext) for ext in extensions):
                            file_path = os.path.join(root, file)
                            relative_path = os.path.relpath(file_path, root_dir)
                            log(f"Processing file: {relative_path}")
                            
                            outfile.write(f"\n\n{'='*80}\n")
                            outfile.write(f"File: {relative_path}\n")
                            outfile.write(f"{'='*80}\n\n")
                            
                            try:
                                with open(file_path, 'r', encoding='utf-8') as infile:
                                    outfile.write(infile.read())
                            except Exception as e:
                                log(f"Error reading file: {file_path}, Error: {e}")
                                outfile.write(f"Error reading file: {str(e)}\n")
        log(f"Processing complete. Output written to: {output_file}")
    except Exception as e:
        log(f"Error writing output file: {output_file}, Error: {e}")

def aggregate_code(root_dir, non_json_output, json_output):
    log(f"Starting aggregation for root directory: {root_dir}")
    
    # Define the directories and file extensions to process
    target_dirs = ['src', 'data']
    non_json_extensions = ['.py', '.html', '.css', '.js', '.xml', '.txt']
    json_extension = ['.json']
    
    log(f"Non-JSON output file: {non_json_output}")
    log(f"JSON output file: {json_output}")
    
    # Process non-JSON files
    process_files_in_dirs(root_dir, target_dirs, non_json_extensions, non_json_output)
    # Process JSON files
    process_files_in_dirs(root_dir, target_dirs, json_extension, json_output)
    
    log("Aggregation complete.")

if __name__ == "__main__":
    root_directory = r"C:\Users\jer43\OneDrive\Documents\GitHub\Deploy_Adventure_Game"
    non_json_output_file = r"C:\Users\jer43\OneDrive\Documents\GitHub\aggregated_code_non_json.txt"
    json_output_file = r"C:\Users\jer43\OneDrive\Documents\GitHub\aggregated_code_json.txt"
    
    aggregate_code(root_directory, non_json_output_file, json_output_file)
