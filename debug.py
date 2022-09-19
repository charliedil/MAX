import cPickle as pickle

pmcid_to_pmid = pickle.load(open("pmcid_to_pmid.pkl","rb"))
pmid_to_mesh = pickle.load(open("pmid_to_mesh.pkl","rb"))

print(pmcid_to_pmid)
print(pmid_to_mesh)
