
from nb_path import NbPath
import nb_log

# For debugging, you can prevent cleanup
with NbPath.tempdir(cleanup=True) as persistent_tmp_dir:
    persistent_tmp_dir.joinpath("log.txt").write_text("some debug info")
    print(f"This directory will NOT be deleted: {persistent_tmp_dir}")

with NbPath.tempfile(suffix=".txt", prefix="config_",cleanup=True,dir=NbPath.self_py_dir()) as tmp_file:
    print(f"Temporary file: {tmp_file}")
    tmp_file.write_text("temporary setting")


with NbPath.tempfile(suffix=".txt", prefix="config_",cleanup=False,dir=NbPath.self_py_dir()) as tmp_file:
    print(f"Temporary file: {tmp_file}")
    tmp_file.write_text("temporary setting")