from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore import InMemoryDocstore
import os
import faiss
import warnings
import logging
warnings.filterwarnings("ignore")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger().setLevel(logging.ERROR)

from transformers import logging as hf_logging
hf_logging.set_verbosity_error()

VECTOR_DATABASE_LOCATION = "D:\\industrial internship\\internship project1\\App\\Vector Store\\vector_store_stellla_en_400M_v5"
TEMPORARY_VECTOR_DATABASE = "D:\\industrial internship\\internship project1\\App\\Vector Store\\temporary_vector_store_stellla_en_400M_v5"

class Model():
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="dunzhang/stella_en_400M_v5",
            model_kwargs={
                "trust_remote_code": True,
                "device": "cpu",
                "config_kwargs": {
                    "use_memory_efficient_attention": False,
                    "unpad_inputs": False
                }
            }
        )
        if os.path.exists(TEMPORARY_VECTOR_DATABASE):
            self.temp_vector_store = FAISS.load_local(TEMPORARY_VECTOR_DATABASE,self.embedding_model,allow_dangerous_deserialization=True)
            self.temp_total_document = len(self.temp_vector_store.index_to_docstore_id)
        else:
            print("\033[91mTemporary vector store does not exist\033[0m")
            self.temp_total_document = 0
        if os.path.exists(VECTOR_DATABASE_LOCATION):
            self.vector_store = FAISS.load_local(VECTOR_DATABASE_LOCATION,self.embedding_model,allow_dangerous_deserialization=True)
            self.total_document = len(self.vector_store.index_to_docstore_id)
        else:
            print("\033[91mVector store does not exist\033[0m")
            self.total_document = 0
        
    def create_embedding(self,input):
        """
        Convert the given text into embedding using the initialized word embedding model

        Args:
            input (str): String to be embed
        
        Returns:
            list: embedding in form of list
        """
        embeddings = self.embedding_model.embed_query(input)
        return embeddings

    def store_in_vectordatabase(self,input):
        """ 
        Add the new document to already exsiting vector database and if not present then create a new database and store the document 

        Args:
            input (str): String to be embed
        
        Returns:
            bool: if document is succesfully added to the vector database
        """
        try:
            text = input
            text_embedding = self.create_embedding(input)
            text_embedding_pair = zip([text],[text_embedding])
            if os.path.exists(VECTOR_DATABASE_LOCATION):
                result = self.vector_store._similarity_search_with_relevance_scores(input)
                if result[0][1] == 1:
                    print("\033[94mSame document already present in the vectore store\033[0m")
                    return True
                else:
                    self.vector_store.add_embeddings(text_embedding_pair)
                    self.vector_store.save_local(VECTOR_DATABASE_LOCATION)
                    print("\033[94mSuccesfully stored embedding in exsiting vector database\033[0m")
                    return True
            else:
                self.vector_store = FAISS.from_embeddings(text_embedding_pair,self.embedding_model)
                self.vector_store.save_local(VECTOR_DATABASE_LOCATION)
                print("\033[92mSuccesfully stored embedding in newly created vector database\033[0m")
                return True
        except Exception as e:
            print("\033[91mUnexpected error occured in storing the embeddings in database :\033[0m",e)
            return False
        
    def store_in_temp_vectordatabase(self,input):
        """ 
        Add the new document to already exsiting temporary vector database and if not present then create a new database and store the document 

        Args:
            input (str): String to be embed
        
        Returns:
            bool: if document is succesfully added to the vector database
        """
        try:
            text = input
            text_embedding = self.create_embedding(input)
            text_embedding_pair = zip([text],[text_embedding])
            if os.path.exists(TEMPORARY_VECTOR_DATABASE):
                result = self.temp_vector_store._similarity_search_with_relevance_scores(input)
                if result != [] and result[0][1] == 1:
                    print("\033[94mSame document already present in the temporary vectore store\033[0m")
                    return True
                else:
                    self.temp_vector_store.add_embeddings(text_embedding_pair)
                    self.temp_vector_store.save_local(TEMPORARY_VECTOR_DATABASE)
                    self.temp_total_document += 1
                    print("\033[94mSuccesfully stored embedding in exsiting temporary vector database\033[0m")
                    return True
            else:
                self.delete_temp_database()
                self.temp_vector_store = FAISS.add_embeddings(text_embedding_pair)
                self.temp_vector_store.save_local(TEMPORARY_VECTOR_DATABASE)
                self.temp_total_document += 1
                print("\033[92mSuccesfully stored embedding in newly created temporary vector database\033[0m")
                return True
        except Exception as e:
            print("\033[91mUnexpected error occured in storing the embeddings in database :\033[0m",e)
            return False
        
    def search_from_database(self,input):
        """ 
        Search the most similar document from the vector database and calculates the similarity score.

        Args:
            input (str): String which is used to find the similarity
        
        Returns:
            dict: similar document along with their similarity score in keys Document and Score
        """
        try:
            score = []
            document = []
            # query = self.create_embedding(input)
            result = self.vector_store._similarity_search_with_relevance_scores(input)
            for i in range(len(result)):
                score.append(result[i][1])
                document.append([str(result[i][0])])
            return {
                "Document":document,
                "Score":score
            }
        except Exception as e:
            print("\033[91mUnexpected error while searching in database :\033[0m",e)

    def search_from_temp_database(self,input):
        """ 
        Search the most similar document from the vector database and calculates the similarity score.

        Args:
            input (str): String which is used to find the similarity
        
        Returns:
            dict: similar document along with their similarity score in keys Document and Score
        """
        try:
            score = []
            document = []
            result = self.temp_vector_store._similarity_search_with_relevance_scores(input)
            print("similarity serach result in search_from_temp_database : ",result)
            print("Number of document in Temp vector store :",self.temp_total_document)
            for i in range(len(result)):
                score.append(result[i][1])
                document.append([str(result[i][0])])
            return {
                "Document":document,
                "Score":score
            }
        except Exception as e:
            print("\033[91mUnexpected error while searching in database :\033[0m",e)
        
    def delete_temp_database(self):
        """
        This Function is used to reset the temporary vectorstore to empty
        """
        embedding_dim = len(self.embedding_model.embed_query("placeholder"))
        index = faiss.IndexFlatL2(embedding_dim)
        self.temp_vector_store = FAISS(
            embedding_function=self.embedding_model,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={}
        )
        self.temp_vector_store.save_local(TEMPORARY_VECTOR_DATABASE)
        print("\033[92mSuccessfully created Temporary vector store\033[0m")