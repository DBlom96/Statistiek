import os
import shutil
import subprocess

# Configuration
num_learning_tasks = 20
output_dir_pdf = "."
output_dir_png = "."

# Ensure output directories exist
os.makedirs(output_dir_pdf, exist_ok=True)
os.makedirs(output_dir_png, exist_ok=True)

for i in range(1, 5):#num_learning_tasks + 1):
    print(f"\n==========================================")
    print(f"COMPILING LEARNING TASK {i}")
    print(f"==========================================")

    # 1. Write the macro to dynamically select the task in main_exercises.tex
    with open("./compilation_macros.tex", "w", encoding="utf-8") as f:
        f.write(f"\\newcommand{{\\learningtask}}{{{i}}}\n")

    # 2. Run pdflatex (run twice for cross-references/TOC)
    print(f"--- Compiling LaTeX (Pass 1) ---")
    subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "./main_questions.tex"],
        check=True,
    )

    if i > 1:
        print(f"--- Compiling LaTeX (Pass 2) ---")
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "./main_questions.tex"],
            check=True,
        )

    # 3. Copy and save the output PDF
    pdf_output_path = os.path.join(output_dir_pdf, f"lt{i}_questions.pdf")
    shutil.copy2("./main_questions.pdf", pdf_output_path)
    print(f"[✓] Saved PDF: {pdf_output_path}")

    # 4. Convert the compiled PDF directly to a high-resolution PNG
    png_prefix = f"lt{i}_temp"
    print(f"--- Converting PDF to PNG (300 DPI) ---")
    subprocess.run(
        ["pdftoppm", "-png", "-r", "300", pdf_output_path, png_prefix],
        check=True,
    )

    # 5. Move/Rename the generated PNG (pdftoppm outputs lt{i}_temp-1.png for single page)
    temp_png = f"{png_prefix}-1.png"
    final_png_path = os.path.join(output_dir_png, f"lt{i}_questions.png")

    if os.path.exists(temp_png):
        shutil.move(temp_png, final_png_path)
        print(f"[✓] Saved PNG: {final_png_path}")
    else:
        print(
            f"[!] Warning: Could not locate converted PNG output ({temp_png})"
        )

    # 6. Clean up generated PDF files
    os.remove(f"./lt{i}_questions.pdf")

print("\nBuild complete. All PDFs and PNGs have been generated!")