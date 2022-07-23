# Compass - Comparison Of Mass Projects And Student Schoolwork

This docker app runs flask and python allowing the user to upload bulk student assignments, in addition to a template (starter) assignment, then scans all student work for likeness. Originally built as a stand alone python script, this repo is an attempt to Dockerize and refine it for ease of use and development.

## Roadmap
- Bulk upload files *(Completed)*
- Upload template assignment *(Completed)*
- Recursively unzip all files *(Completed)*
- Generate randomized alphanumeric session sequence *(Partially Completed)*
- OCR all PDF's
- Convert docx files to txt
- Direct file compare
- Collect results for ease of display
- Display results
- Cleanup/remove files after 14 days


## Future Plans
- Compare line likeness (look for 1 or 2 words that were altered/removed/added and still label line as matching)
- Clean and color code similar lines/paragraphs in the results
