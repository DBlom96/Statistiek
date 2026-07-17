import subprocess
import os

# Configuration
num_chapters = 13
chapters = []

for i in range(1, num_chapters + 1):
    print(f"COMPILING WEEK {i}")
    
    # Skip week 7
    if i == 7:
        continue

    # Build the chapter string
    if i < 10:
        chapters.append(f"0{i}")
    else:
        chapters.append(str(i))
    
    # Write the includeonly list to the file
    with open("./enabled_chapters.tex", "w") as f:
        f.write(f"\\foreach \\week in" + "{" + ", ".join(chapters) + "}\n")
        f.write("{\n")
        f.write("\t\\input{./huiswerk/week\\week.tex}\n")
        f.write("}\n")

    
    print(f"--- Compiling step {i} ---")
    
    # Run pdflatex (run twice for TOC/references)
    subprocess.run(["pdflatex", "-interaction=nonstopmode", "./main.tex"], check=True)
    if i > 1:
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "./main.tex"], check=True)
    
    print("We reacht hsi")
    # Copy the resulting PDF (Moved inside the loop)
    output_name = f"./uitwerkingen_week_0{i}.pdf" if i < 10 else f"./uitwerkingen_week_{i}.pdf"
    
    # Use shutil.copy2 instead of os.replace so the original main.pdf isn't deleted
    import shutil
    shutil.copy2("./main.pdf", output_name)
    print(f"Saved: {output_name}")

print("Build complete.")