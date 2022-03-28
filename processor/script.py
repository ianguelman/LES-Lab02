import sys, os, json
import numpy as np

def main():
    repo_url: str = sys.argv[1]
    os.system("git clone {} --filter=blob:none /git".format(repo_url))
    os.system("java -jar /usr/bin/ck.jar /git false 0 False /tmp/")
    os.system("csv-to-json /tmp/class.csv /tmp/class.json")
    file = open('/tmp/class.json')
    data = json.load(file)

    attributes = {
        'dit': 0,
        'loc' : [],
        'cbo' : [],
        'cbo:mean': 0.0,
        'cbo:median': 0.0,
        'cbo:std': 0.0,
        'lcom*' : [],
        'lcom*:mean': 0.0,
        'lcom*:median': 0.0,
        'lcom*:std': 0.0
    }
    
    for d in data:
        for metric in ['loc', 'cbo', 'lcom*']:
            if d[metric] != 'NaN':
                attributes[metric] += [float(d[metric])]
        if float(d['dit']) > attributes['dit']:
            attributes['dit'] = float(d['dit'])
    
    for metric in ['cbo', 'lcom*']:
        attributes[metric+':mean'] = np.mean(attributes[metric])
        attributes[metric+':median'] = np.median(attributes[metric])
        attributes[metric+':std'] = np.std(attributes[metric])
        del attributes[metric]

    attributes['loc'] = np.sum(attributes['loc'])

    print(json.dumps(attributes).replace('NaN', r'"Not processed."'))
    
main()
    