# myapp/management/commands/import_tsv.py

import os
import csv
from django.core.management.base import BaseCommand
from biomdata.models import Taxonomy

class Command(BaseCommand):
    help = 'Imports data from all .tsv files found in the downloads directory into the Taxonomy model'

    def handle(self, *args, **kwargs):
        base_dir = '/app'
        downloads_dir = os.path.join(base_dir, 'downloads')
        pass
        
        if not os.path.isdir(downloads_dir):
            self.stderr.write(f"Directory {downloads_dir} does not exist")
            return

        # List all .tsv files in the directory
        tsv_files = [f for f in os.listdir(downloads_dir) if f.endswith('.tsv')]
        
        if not tsv_files:
            self.stdout.write("No .tsv files found in the downloads directory.")
            return
        
        # Process each .tsv file
        for tsv_file in tsv_files:
            file_path = os.path.join(downloads_dir, tsv_file)
            
            # Print the file name
            self.stdout.write(f"\nProcessing file: {tsv_file}")
            
            # Import data from the file
            self.import_tsv(file_path)

    def import_tsv(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                Taxonomy.objects.create(
                    name=row['Name'],
                    tax_id=row['Tax ID'],
                    abundance_score=row['Abundance Score'],
                    relative_abundance=row['Relative Abundance'],
                    unique_matches_frequency=row['Unique Matches Frequency'],
                )
                self.stdout.write(f"Created new record: {row['Name']}")
