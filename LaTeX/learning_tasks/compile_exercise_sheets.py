import subprocess
import os

# Configuration
num_learning_tasks = 14

for i in range(14, num_learning_tasks + 1):
    print(f"COMPILING LEARNING TASK {i}")
        
    # Write the includeonly list to the file
    with open("./compilation_macros.tex", "w") as f:
        f.write(f"\\newcommand{{\\learningtask}}{{{i}}}")

    
    print(f"--- Compiling step {i} ---")
    
    # Run pdflatex (run twice for TOC/references)
    subprocess.run(["pdflatex", "-interaction=nonstopmode", "./main_exercises.tex"], check=True)
    if i > 1:
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "./main_exercises.tex"], check=True)
    
    # Copy the resulting PDF (Moved inside the loop)
    output_name = f"./ExerciseSheets/lt{i}_exercises.pdf"
    
    # Use shutil.copy2 instead of os.replace so the original main.pdf isn't deleted
    import shutil
    shutil.copy2("./main_exercises.pdf", output_name)
    print(f"Saved: {output_name}")

print("Build complete.")