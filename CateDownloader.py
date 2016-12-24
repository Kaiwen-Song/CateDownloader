from NetworkLibrary import *
import argparse
#get the directory and login in formation from the user

#get the year and courses the user wishes to download

#create and navigate to the directory

#downlaod the files to the corresponding directory

Download_Path = "~/Downloads"
Download_Folder = Download_Path + "/Cate_Stuff"

parser = argparse.ArgumentParser()
parser.add_argument("-all")
args = parser.parse_args()

agent = mechanize.Browser()
username, password = get_user_credentials()
agent.add_password(Cate_URL, username, password)

agent.set_handle_robots(True)
# year = get_year_of_access()
# class_code = get_class_code()
year = "2016"
class_code = "c4"
cate_string = format_cate_string(class_code, year, username)
print(cate_string)
agent.open(cate_string)
create_directory(Download_Folder)
download_file(agent, Download_Folder, "",Download_Folder+"/test")
