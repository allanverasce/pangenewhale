#!/usr/bin/env python3

"""
Pangenome Category Calculator

This script calculates the pangenome categories (hard core, soft core, shell, cloud)
based on a set of GenBank files and a protein cluster file (e.g., from Panakeia, Roary, or Panaroo).

It works in three main steps:
1.  Maps every gene (locus_tag) from all GenBank files to its source genome ID.
2.  Reads the cluster file line by line.
3.  For each cluster, it checks how many *unique* genomes are represented.
4.  It classifies the cluster into a pangenome category based on its frequency
    across the total number of genomes.

Requirements:
    - Biopython (pip install biopython)
"""

import os
from Bio import SeqIO
import sys # Used for exit()

# ==============================================================================
# === 1. CONFIGURATION: SET YOUR PATHS AND THRESHOLDS ===
# ==============================================================================

# --- (Required) Paths for input files ---
# TODO: Update these paths to point to your files
gbk_directory = "/path/to/your/genbank/directory"
clusters_filepath = "/path/to/your/protein_clusters.txt"

# --- (Optional) Pangenome category thresholds ---
# These fractions define the boundaries for each category.
# Default values are common in pangenome literature.

# Hard core: Genes present in >= 99% of genomes
HARD_CORE_THRESHOLD = 0.99
# Soft core: Genes present in >= 95% (but < 99%)
SOFT_CORE_THRESHOLD = 0.95
# Shell: Genes present in >= 15% (but < 95%)
SHELL_THRESHOLD = 0.15
# Cloud: Genes present in < 15% of genomes

# ==============================================================================
# === 2. Step 1: Map all genes (locus_tags) to their source genomes ===
# ==============================================================================

print(f"--- Step 1: Mapping genes (locus_tags) to their source genomes ---")

# This dictionary will store the mapping: { 'locus_tag_XYZ': 'genome_ID_A' }
locus_tag_to_genome_map = {}

# Check if the GenBank directory exists
if not os.path.isdir(gbk_directory):
    print(f"ERROR: Directory not found: '{gbk_directory}'")
    print("Please update the 'gbk_directory' variable in the script.")
    sys.exit(1) # Exit with an error code

# Find all GenBank files in the specified directory
# Common extensions are .gbk, .gb, or .genbank
genome_files = [f for f in os.listdir(gbk_directory) if f.endswith(('.gbk', '.gb', '.genbank'))]
total_genomes = len(genome_files)

# Check if we found any genomes
if total_genomes == 0:
    print(f"ERROR: No GenBank (.gbk, .gb, .genbank) files found in '{gbk_directory}'")
    print("Please check your path.")
    sys.exit(1)

print(f"Found {total_genomes} genome files. Parsing all CDS features...")

for filename in genome_files:
    # Use the filename (without extension) as the unique genome ID
    genome_id = os.path.splitext(filename)[0]
    gbk_path = os.path.join(gbk_directory, filename)

    try:
        # Parse each GenBank file
        # A single .gbk file can contain multiple records (contigs)
        for record in SeqIO.parse(gbk_path, "genbank"):
            # Iterate through all features (genes, CDS, rRNA, etc.)
            for feature in record.features:
                # We only care about protein-coding sequences (CDS)
                # and only if they have a 'locus_tag' qualifier
                if feature.type == "CDS" and 'locus_tag' in feature.qualifiers:
                    # Get the locus_tag (it's a list, so we take the first element)
                    locus_tag = feature.qualifiers['locus_tag'][0]
                    
                    # Store the mapping
                    if locus_tag in locus_tag_to_genome_map:
                        # This should not happen if locus_tags are truly unique
                        print(f"Warning: Duplicate locus_tag '{locus_tag}' found. Overwriting.")
                    
                    locus_tag_to_genome_map[locus_tag] = genome_id
                    
    except Exception as e:
        print(f"Warning: Could not parse file {filename}. Error: {e}")
        print("This file will be skipped.")
        total_genomes -= 1 # Decrement count if file is bad

print(f"Mapping complete. Found {len(locus_tag_to_genome_map)} total CDS features across {total_genomes} valid genomes.\n")


# ==============================================================================
# === 3. Step 2: Analyze cluster file and count genome presence ===
# ==============================================================================

print(f"--- Step 2: Analyzing cluster file '{clusters_filepath}' ---")

# Initialize counters for each pangenome category
pangenome_category_counts = {
    'hard_core': 0,
    'soft_core': 0,
    'shell': 0,
    'cloud': 0
}

# Check if cluster file exists
if not os.path.isfile(clusters_filepath):
    print(f"ERROR: Cluster file not found: '{clusters_filepath}'")
    print("Please update the 'clusters_filepath' variable in the script.")
    sys.exit(1)

total_clusters_analyzed = 0

# Open and read the cluster file line by line
# Assumes a space-delimited format like: Cluster_ID_001 <locus_tag_1> <locus_tag_2> ...
try:
    with open(clusters_filepath, 'r') as f:
        for line in f:
            parts = line.strip().split()
            
            # Skip empty lines
            if not parts:
                continue

            total_clusters_analyzed += 1
            
            # The first part is the cluster ID (e.g., "group_1"), 
            # the rest are the locus_tags that belong to it.
            locus_tags_in_cluster = parts[1:]

            # Use a set to store the *unique* genome IDs found in this cluster.
            # This is crucial for handling paralogs (multiple genes from the
            # same genome in one cluster) correctly.
            genomes_in_cluster = set()
            
            for tag in locus_tags_in_cluster:
                # Look up the genome ID for each locus_tag
                if tag in locus_tag_to_genome_map:
                    # Add the genome ID to the set.
                    # Duplicates will be ignored automatically by the set.
                    genomes_in_cluster.add(locus_tag_to_genome_map[tag])
                else:
                    # This can happen if the cluster file includes tags
                    # not found in the GenBank files (e.g., from different annotations)
                    # print(f"Warning: Locus tag '{tag}' from cluster file not found in GenBank data. Skipping tag.")
                    pass

            # Calculate the fraction of genomes that have this gene cluster
            num_genomes_in_cluster = len(genomes_in_cluster)
            fraction = num_genomes_in_cluster / total_genomes

            # Classify the cluster based on the thresholds
            if fraction >= HARD_CORE_THRESHOLD:
                pangenome_category_counts['hard_core'] += 1
            elif fraction >= SOFT_CORE_THRESHOLD:
                pangenome_category_counts['soft_core'] += 1
            elif fraction >= SHELL_THRESHOLD:
                pangenome_category_counts['shell'] += 1
            else:
                pangenome_category_counts['cloud'] += 1

except Exception as e:
    print(f"ERROR: Failed to read or process cluster file: {e}")
    sys.exit(1)
    
print(f"Cluster analysis complete. Processed {total_clusters_analyzed} clusters.\n")


# ==============================================================================
# === 4. Step 3: Display the results ===
# ==============================================================================

print("--- Pangenome Analysis Results ---")
print(f"Total genomes analyzed: {total_genomes}")
print(f"Total clusters (gene families) analyzed: {total_clusters_analyzed}")
print("---")
print(f"Hard core genes (>= {int(HARD_CORE_THRESHOLD*100)}%): {pangenome_category_counts['hard_core']}")
print(f"Soft core genes (>= {int(SOFT_CORE_THRESHOLD*100)}%): {pangenome_category_counts['soft_core']}")
print(f"Shell genes (>= {int(SHELL_THRESHOLD*100)}%): {pangenome_category_counts['shell']}")
print(f"Cloud genes (< {int(SHELL_THRESHOLD*100)}%): {pangenome_category_counts['cloud']}")
print("---")

# Sanity check
total_counted = sum(pangenome_category_counts.values())
if total_counted != total_clusters_analyzed:
    print(f"Warning: Total counted clusters ({total_counted}) does not match total analyzed ({total_clusters_analyzed}).")

print("Script finished.")
