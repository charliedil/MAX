import pickle
import shutil
mesh_terms = ["acute kidney injury"]

pmcid_to_mesh = pickle.load(open("pmcid_to_mesh.pkl", "rb"))

pmcids = []

for pmcid in pmcid_to_mesh:
    for mesh in pmcid_to_mesh[pmcid]:
        if mesh in mesh_terms:
            pmcids.append(pmcid+".txt")
print(pmcids)

for f in pmcids:
    shutil.copyfile("PMC085XXXXX_txt/"+f, "pmc_input_files/"+f)
