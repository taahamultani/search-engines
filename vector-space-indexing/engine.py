class VectorCompare:

    def __init__(self, repository):
        """
        Initialize VectorCompare with a Repository instance
        to access the calculate_tf method
        """
        self.repo = repository

    def magnitude(self, document):
        ''' 
        Returns the magnitude of the document 
        i.e |v|
        '''

        val = 0
        for i, v in document.items():
            val += v ** 2
        
        return val ** 0.5
    
    def compare(self, search_query, document):
        ''' 
        Returns the cosine similarity between search query and document
        i.e (a.b) / (|a|.|b|)
        '''
        # Use calculate_tf from Repository class to convert search query string to term frequencies
        search_query_tf = self.repo.calculate_tf(search_query)

        dot_product = 0
        for i, v in search_query_tf.items():
            if i in document:
                dot_product += (v * document[i])
        
        magnitudes = self.magnitude(search_query_tf) * self.magnitude(document)

        return dot_product / magnitudes
    
class Repository:
    documents = {}
    document_texts = {}
    counter = 0

    def calculate_tf(self, document):
        '''
        Calculate term frequencies
        '''

        val = {}
        for word in document.split(' '):
            val[word] = val.get(word,0) + 1
        
        return val

    def index_page(self, document):
        '''
        Index a document by storing the term frequencies and original text
        '''

        self.counter += 1
        # Store the term frequencies for comparison
        self.documents[self.counter] = self.calculate_tf(document)
        # Store the original document text for display
        self.document_texts[self.counter] = document

    def get_documents(self):
        '''
        Return all indexed documents (term frequencies)
        '''

        return self.documents
    
    def get_document_text(self, doc_id):
        '''
        Return the original text of a specific document
        '''

        return self.document_texts.get(doc_id, "")


if __name__ == '__main__':
    import os

    repo = Repository()
    
    # Index all documents
    documents_folder_path = os.path.join(os.getcwd(), 'vector-space-indexing', 'documents')
    for file in os.listdir(documents_folder_path):
        file_path = os.path.join(documents_folder_path,file)
        with open(file_path,'r') as f:
            repo.index_page(f.read().lower())
    
    # Get the search query
    search_query = input("Enter search query: ").lower()

    comp = VectorCompare(repo)

    matches = []
    # Iterate over the document values, not just the keys
    for doc_id, document in repo.get_documents().items():
        score = comp.compare(search_query, document)
        if score != 0:
            # Store document ID along with score for reference
            matches.append([score, doc_id])
    
    matches.sort(reverse=True)

    # Display results with actual document content
    for score, doc_id in matches:
        doc_text = repo.get_document_text(doc_id)
        # Display first 100 characters of the document
        preview = doc_text[:100] if len(doc_text) > 100 else doc_text
        print(f"{score} - {preview}")