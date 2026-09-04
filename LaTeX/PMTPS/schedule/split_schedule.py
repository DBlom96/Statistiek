import subprocess

TOTAL_TASKS = 20
MAIN_TEX = "schedule"

for lt in range(1, TOTAL_TASKS + 1):
    print(f"Compiling LT {lt}...")
    cmd = [
        "pdflatex",
        "-interaction=nonstopmode",
        f"-jobname=./schedule_LT{lt}",
        f"\\def\\learningtask{{{lt}}}\\input{{{MAIN_TEX}.tex}}"
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("Done! Generated 20 tailored PDF sheets.")