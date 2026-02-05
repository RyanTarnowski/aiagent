from functions.get_files_info import get_files_info

print("Result for current directory:")
print(get_files_info("calculator", "."))
# Result for current directory:
#   - main.py: file_size=719 bytes, is_dir=False
#   - tests.py: file_size=1331 bytes, is_dir=False
#   - pkg: file_size=44 bytes, is_dir=True

print("Result for 'pkg' directory:")
print(get_files_info("calculator", "pkg"))
# Result for 'pkg' directory:
#   - calculator.py: file_size=1721 bytes, is_dir=False
#   - render.py: file_size=376 bytes, is_dir=False

print("Result for '/bin' directory:")
print(get_files_info("calculator", "/bin"))
# Result for '/bin' directory:
#     Error: Cannot list "/bin" as it is outside the permitted working directory

print("Result for '../' directory:")
print(get_files_info("calculator", "../"))
# Result for '../' directory:
#     Error: Cannot list "../" as it is outside the permitted working directory
