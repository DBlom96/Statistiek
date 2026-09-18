import subprocess
import os

# Configuration
num_lectures = 4

for i in range(1, num_lectures + 1):
    print(f"Compileer college {i}")
    
    # Write the includeonly list to the file
    with open("./enabled_lectures.tex", "w") as f:
        f.write("\\input{../colleges/college_" + str(i) + "_P&S.tex}\n")
    
    # Run pdflatex (run twice for TOC/references)
    subprocess.run(["pdflatex", "-interaction=nonstopmode", "./main.tex"], check=True)
    if i > 1:
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "./main.tex"], check=True)
    
    # Copy the resulting PDF (Moved inside the loop)
    output_name = f"../P&S2026_college_{i}.pdf"
    
    # Use shutil.copy2 instead of os.replace so the original main.pdf isn't deleted
    import shutil
    shutil.copy2("./main.pdf", output_name)
    print(f"Saved: {output_name}")

print("Build complete.")