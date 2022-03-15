import sys, os, json

def main():
    repo_url: str = sys.argv[1]
    os.system("git clone {} --filter=blob:none /git".format(repo_url))
    os.system("java -jar /usr/bin/ck.jar /git false 0 False /tmp/")
    os.system("csv-to-json /tmp/class.csv /tmp/class.json")
    file = open('/tmp/class.json')
    data = json.load(file)

    attributes = {
        'dit': float(data[0]['dit']),
        'loc': 0.0,
        'cbo': 0.0,
        'lcom*': 0.0
    }
    
    for d in data:
        attributes['loc'] += int(d['loc'])
        attributes['cbo'] += int(d['cbo'])
        attributes['lcom*'] += int(d['lcom*'])
        
    attributes['cbo'] = attributes['cbo']/len(data)
    attributes['lcom*'] = attributes['lcom*']/len(data)
    
    print(attributes)
    
main()