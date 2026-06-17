import os
import sys
import subprocess
import logging

#Logging configuration
logging.basicConfig(
    filename="logs/log_test.log",
    format='%(asctime)s %(levelname)s: %(message)s',
    filemode='a'
)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def run_script(script_path):
    """
    Executes a python script safely as a subprocess.
    Logs tracking updates dynamically to the log file instead of stdout.
    """
    script_name = os.path.basename(script_path)
    logger.info(f"Orchestrator: Initializing pipeline execution step -> {script_path}")

    try:
        subprocess.run(
            [sys.executable, script_path],
            check=True,          # Automatically triggers CalledProcessError if return code != 0
            text=True,
            capture_output=True 
        )
        logger.info(f"Orchestrator: Successfully completed -> {script_name} (Exit Code 0)")
        return True

    except subprocess.CalledProcessError as e:
        logger.critical(
            f"Orchestrator Failure: Pipeline step collapsed at {script_name}. "
            f"Exit Code: {e.returncode}. Execution halted defensively."
        )
        # Capture and log standard error stream messages from the failing child process
        if e.stderr:
            logger.error(f"Child process error track: {e.stderr.strip()}")
        return False
    except Exception as e:
        logger.critical(f"Orchestrator Error: Structural exception trying to spin up {script_name}. Reason: {e}")
        return False


if __name__ == "__main__":
    logger.info("STARTING PIPELINE RUN CYCLE")

    pipeline_steps = [
        os.path.join("Processing", "ingest.py"),
        os.path.join("Processing", "transform.py"),
        os.path.join("Processing", "analyze.py"),
        os.path.join("Processing", "visualize.py"),
        "report.py"
    ]

    pipeline_success = True

    for step in pipeline_steps:
        if not run_script(step):
            pipeline_success = False
            break  # Break cycle early if any script returns an exit code of 1

    if pipeline_success:
        logger.info("PIPELINE COMPLETED WORKFLOW SUCCESSFULLY")
        sys.exit(0)
    else:
        logger.error("PIPELINE TERMINATED WITH ERRORS BEFORE COMPLETION")
        sys.exit(1)