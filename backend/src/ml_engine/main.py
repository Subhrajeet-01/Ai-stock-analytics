
# import sys
# from pathlib import Path

# # 1. Get the path to the current notebook directory (ml_engine)
# current_dir = Path.cwd()

# # 2. Navigate up three levels to reach the project root ('Ai-stock-analytics')
# # Current: ml_engine
# # Parent: src
# # Grandparent: backend
# # Great-Grandparent: Ai-stock-analytics (This is the required path)
# project_root = current_dir.parent.parent.parent 
# print(f"current_dir: {current_dir}")
# print(f"project_root: {project_root}")
# # 3. Add the project root to sys.path
# if str(project_root) not in sys.path:
#     sys.path.insert(0, str(project_root))

# print(f"Project root added to sys.path: {project_root}")
# print("\nNew sys.path:")
# for path in sys.path:
#     print(path)

from backend.src.database.connect import engine 
if __name__ == "__main__":
    
    print("ML Engine main executed")