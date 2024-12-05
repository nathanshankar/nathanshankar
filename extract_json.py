import shutil
import os
from submodules.serp_api_extracter.utils.utils import extract_json_and_save
#shutil.copyfile('./submodules/serp_api_extracter/data.json', 'google_scholar_nathan.json')


def main() -> None:
    base_path = os.getcwd()
    my_json = base_path + '/' + 'google_scholar_nathan.json'
    extract_json_and_save(my_json)


if __name__ == "__main__":
    main()
