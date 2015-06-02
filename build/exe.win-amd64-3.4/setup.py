from cx_Freeze import setup, Executable

setup(
	name="SamConverter",
	version="0.1",
	description="Finds midpoints of black",
	executables=[Executable("SamConverter.py")] ,
)