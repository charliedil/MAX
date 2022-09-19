import os
from medacy.data import Dataset
from medacy.pipelines import LstmSystematicReviewPipeline
from medacy.model.model import Model
import re
import pickle
categories = ["consult", "discharge_summary", "general", "nursing", "pharmacy", "physician"]
entities = ["Drug", "Route", "Form", "Reason", "Duration", "Frequency", "ADE", "Strength", "Dosage"]

pipeline = LstmSystematicReviewPipeline(metamap=None, entities=entities, word_embeddings="../medacy/word_embeddings/mimic3_d200.txt", cuda_device=0)
model = Model(pipeline)
output_file_path = 'gene_lstm.p'
training_dataset = Dataset("output/")
model.fit(training_dataset)

#model.dump(output_file_path)
pickle.dump(model, open(output_file_path, "wb"))
# done training, start test


