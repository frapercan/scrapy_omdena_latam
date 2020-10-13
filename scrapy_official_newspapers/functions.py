import urllib
import os




def download_doc_url(item):

    filename = item['source'] + "/" + item['reference'] + "." + item['doc_type']
    directory = filename.split("/")[-2]
    name = filename.split("/")[-1]
    dir = os.path.join(os.path.dirname(__file__), os.path.join('downloaded', directory))
    dir_name = os.path.join(os.path.dirname(__file__), os.path.join('downloaded', os.path.join(directory, name)))

    if not os.path.exists(dir):
        os.makedirs(dir)
    urllib.request.urlretrieve(item['doc_url'], filename=dir_name)
