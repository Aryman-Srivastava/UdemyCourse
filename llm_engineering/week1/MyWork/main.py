import sys
import os

if __name__ == "__main__":
    # Relaunch this file with streamlit if not already running under streamlit
    if not any("streamlit" in arg for arg in sys.argv):
        os.system(f'streamlit run router.py')
        sys.exit()
