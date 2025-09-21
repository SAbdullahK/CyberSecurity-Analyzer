import json
import re
from sentence_transformers import SentenceTransformer
import chromadb
import os

class ContextualAnalyzer:
    def __init__(self, gemini_client=None, kb_dir="intelligence/knowledge_base"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.kb_dir = kb_dir
        self.gemini = gemini_client
        self.client = chromadb.PersistentClient(path=".rag_db")
        self.collection = self.client.get_or_create_collection("threat_docs")
        self._load_knowledge_base()

    def _load_knowledge_base(self):
        for fname in os.listdir(self.kb_dir):
            if fname.endswith(".md"):
                with open(os.path.join(self.kb_dir, fname), "r") as f:
                    content = f.read()
                    doc_id = fname.replace(".md", "")
                    self.collection.add(
                        documents=[content],
                        metadatas=[{"source": fname}],
                        ids=[doc_id]
                    )

    def retriever_context(self, query_text, top_k=2):
        results = self.collection.query(
            query_texts=[query_text],
            n_results=top_k
        )
        return results["documents"][0] if results["documents"] else []

    # 🔹 JSON sanitizer
    def _sanitize_json(self, text):
    # If Gemini already gave us a dict, return it
        if isinstance(text, dict):
            return text

        # Clean wrappers
        cleaned = re.sub(r"```json|```", "", str(text)).strip()

        # Try standard JSON
        try:
            return json.loads(cleaned)
        except Exception:
            pass

        # Try Python dict (single quotes, ast eval)
        import ast
        try:
            return ast.literal_eval(cleaned)
        except Exception:
            pass

        # Fallback
        return {"error": "Invalid JSON from Gemini", "raw": text}


    def enhenced_explaination(self, anomaly, severity, context):
        query = f"Anomaly: {anomaly}, Context: {context}"
        retrieved_docs = self.retriever_context(query)

        base_prompt = f"""
        Cybersecurity anomaly detected.
        
        Anomaly : {anomaly}
        Severity : {severity}
        Context : {context}

        Knowledge Base:
        {'\n---\n'.join(retrieved_docs)}

        Please analyze and respond.
        """

        structured_prompt = f"""
        You are a cybersecurity assistant. 
        Always respond in STRICT JSON with the following keys:

        {{
        "threat_type": "string",
        "known_attack": "Yes/No",
        "recommended_actions": ["action1", "action2", "action3"]
        }}

        Input:
        {base_prompt}
        """

        if self.gemini:
            raw_output = self.gemini.generate(structured_prompt)
            return self._sanitize_json(raw_output)   # ✅ always clean before return
        else:
            return {"summary": "Gemini not available.", "docs": retrieved_docs}




# from sentence_transformers import SentenceTransformer
# import chromadb
# # from chromadb.config import Settings
# import os

# class ContextualAnalyzer:
#     def __init__(self, gemini_client = None, kb_dir = "intelligence/knowledge_base"):
#         self.model = SentenceTransformer("all-MiniLM-L6-v2")
#         self.kb_dir = kb_dir
#         self.gemini = gemini_client

#         self.client = chromadb.PersistentClient(path=".rag_db")


#         self.collection = self.client.get_or_create_collection("threat_docs")

#         self._load_knowledge_base()

#     def _load_knowledge_base(self):
#         for fname in os.listdir(self.kb_dir):
#             if fname.endswith(".md"):
#                 with open(os.path.join(self.kb_dir, fname), "r") as f:
#                     content = f.read()
#                     doc_id = fname.replace(".md", "")
#                     self.collection.add(
#                         documents = [content],
#                         metadatas= [{"source" : fname}],
#                         ids = [doc_id]
#                     )
    
#     def retriever_context(self, query_text, top_k=2):
#         results = self.collection.query(
#             query_texts= [query_text],
#             n_results = top_k
#         )
#         return results["documents"][0] if  results["documents"] else []
    
#     def enhenced_explaination(self, anomaly, severity, context):
#         query = f"Anomaly: {anomaly}, Context: {context}"
#         retrieved_docs = self.retriever_context(query)

#         # Core analysis text
#         base_prompt = f"""
#         Cybersecurity anomaly detected.
        
#         Anomaly : {anomaly}
#         Severity : {severity}
#         Context : {context}

#         Knowledge Base:
#         {'\n---\n'.join(retrieved_docs)}

#         Please analyze and respond.
#         """

#         # === Force Gemini into JSON format ===
#         structured_prompt = f"""
#         You are a cybersecurity assistant. 
#         Always respond in STRICT JSON with the following keys:

#         {{
#         "threat_type": "string",
#         "known_attack": "Yes/No",
#         "recommended_actions": ["action1", "action2", "action3"]
#         }}

#         Input:
#         {base_prompt}
#         """

#         if self.gemini:
#             return self.gemini.generate(structured_prompt)  # ✅ structured response
#         else:
#             return {"summary": "Gemini not available.", "docs": retrieved_docs}


        