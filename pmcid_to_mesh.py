import argparse
import requests
import sys
import os
import re
import pickle
import time
#pmc_dir = sys.argv[1] #directory of PMC files
parser = argparse.ArgumentParser(description="Run PMC file MEsH term finder")
parser.add_argument("--input_dir", help = "Path to directory of PMC files", required=True)
parser.add_argument("--pmid_file", help = "Path to pmcid to pmid pickle file - OPTIONAL")
args=parser.parse_args()
if args.pmid_file == None:
    pmc_ids = [] #where we'll store the PMC IDs
    pmcid_to_pmid = {} #map the PMC Id to the PM Id
    no_pmid = []
    for filename in os.listdir(args.input_dir):
        pmc_ids.append(filename.split(".")[0]) #append PMC ids from filenames to list
    chunks = [pmc_ids[x:x+200] for x in range (0,len(pmc_ids),200)] #split into chunks of 200
    for c in chunks:
        input_str = ""
        for i in range(len(c)):
            input_str+=c[i]
            if i!=len(c)-1:
                input_str+=","
        testing = requests.get("https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/", params={"tool":"pmcid_to_mesh", "email":"ndil@vcu.edu", "ids":input_str})
        time.sleep(1)
        print(testing.text)
        records = testing.text.split("<record")
        for r in range(1, len(records)):
            pmid = re.search(r"pmid=\"(.*?)\"", records[r])
            pmcid= re.search(r"pmcid=\"(.*?)\"", records[r]).group(1)
            if pmid:
                pmid = pmid.group(1)
                pmcid_to_pmid[pmcid]=pmid
            else:
                no_pmid.append(pmcid)
    print(pmcid_to_pmid)
    pickle.dump(pmcid_to_pmid, open("pmcid_to_pmid.pkl","wb"))
    pickle.dump(no_pmid, open("no_pmid.pkl", "wb"))
    pmids = list(pmcid_to_pmid.values())
    batches = [pmids[x:x+200] for x in range (0,len(pmids),200)] 
    pmid_to_mesh = {}
    for batch in batches:
        input_str = ""
        for i in range(len(batch)):
            input_str+=batch[i]
            if i!=len(batch)-1:
                input_str+=","

        testing = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi", params={"db":"pubmed","id":input_str,"retmode":"text", "rettype":"medline"})
        print(testing.text)
        output = testing.text
        outputs_split = output.split("\n\n")
        print(len(outputs_split))
        for o in outputs_split:
            pmid=re.search(r"PMID-\s(.*?)\n",o)
            if pmid:
                print(pmid.group(1))
                pmid_to_mesh[pmid] = []
            mesh = re.findall(r"OT\s\s-\s(.*?)\n", o)
            pmid_to_mesh[pmid] = mesh
            time.sleep(1)
    pmcid_to_mesh = {}
    for key in pmcid_to_pmid:
        pmcid_to_mesh[key] = pmid_to_mesh[pmcid_to_pmid[key]]
    print(pmcid_to_mesh)
    pickle.dump(pmcid_to_mesh, open("pmcid_to_mesh.pkl", "wb"))
else:
    pmcid_to_pmid = pickle.load(open(args.pmid_file, "rb"))
   # print(pmcid_to_pmid)
    pmids = list(pmcid_to_pmid.values())
    batches = [pmids[x:x+200] for x in range (0,len(pmids),200)] 
    pmid_to_mesh = {}
    for batch in batches:
        input_str = ""
        for i in range(len(batch)):
            input_str+=batch[i]
            if i!=len(batch)-1:
                input_str+=","

        testing = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi", params={"db":"pubmed","id":input_str,"retmode":"text", "rettype":"medline"})
       # print(testing.text)
        output = testing.text
        outputs_split = output.split("\n\n")
        #print(len(outputs_split))
        for o in outputs_split:
            pmid=re.search(r"PMID-\s(.*?)\n",o)
            if pmid:
              #  print(pmid.group(1))
                pmid_to_mesh[pmid.group(1)] = []
            mesh = re.findall(r"OT\s\s-\s(.*?)\n", o)
           # print(mesh)
           # print(type(mesh))
            pmid_to_mesh[pmid.group(1)] = mesh
        #print(pmid_to_mesh)
        time.sleep(1)
    print(pmid_to_mesh) 
    pmcid_to_mesh = {}
    no_response = []
    for key in pmcid_to_pmid:
        if pmcid_to_pmid[key] in pmid_to_mesh:
            pmcid_to_mesh[key] = pmid_to_mesh[pmcid_to_pmid[key]]
        else:
            no_response.append(pmcid_to_pmid[key])
    print(pmcid_to_mesh)
    print(no_response)
    pickle.dump(pmid_to_mesh, open("pmid_to_mesh.pkl", "wb"))
    pickle.dump(pmcid_to_mesh, open("pmcid_to_mesh.pkl", "wb"))
    pickle.dump(no_response, open("no_response.pkl", "wb"))
    print("done!")
