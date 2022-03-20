from utils.mongo import Mongo
import os, json, subprocess, re

def run():
    # documents = Mongo().get_all_documents()
    url = "https://github.com/spring-projects/spring-boot"
    has_docker_image = os.popen('docker image ls | grep lab02-processor-script').read()
    if not has_docker_image:
        os.system('cd processor && docker build . -t lab02-processor-script')
    proc = subprocess.Popen(
        ['docker', 'run', 'lab02-processor-script', url], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT
    )
    output = re.search(r'({.*})', str(proc.communicate()[0])).group(1)
    parsed_json = json.loads(output)
    Mongo().update_one({'url': url}, {'$set' : parsed_json })
    Mongo().update_one({'url': url}, {'$set' : { 'processed': True } })
    print (f"Métricas salvas do repositório {url}")
    # for doc in documents:
        # result = os.popen('docker run lab02-processor-script {}'.format(doc['url'])).read()
        # print(documents[0]['url'])