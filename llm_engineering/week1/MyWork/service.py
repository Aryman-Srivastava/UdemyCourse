import ollama
from typing import Optional

class LLMService:

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.OLLAMA_API = "http://localhost:11434/api/chat"
        self.chat_history = [self._generate_system_prompt()]
        

    def _generate_response(self, role: str, message: list[dict]):
        response = ollama.chat(model=self.model_name, messages=message)
        return response['message']['content']
    

    def _generate_system_prompt(self):
        return {"role": "system", "content": "You are a helpful assistant."}
    

    def _analyze_code(self, code: Optional[str]):
        prompt = f"Analyze the following code and provide a summary:\n{code}"
        self.chat_history.append({"role": "user", "content": prompt})

        messages = [{"role": "user", "content": prompt}]
        response = self._generate_response(role="user", message=messages)
        self.chat_history.append({"role": "assistant", "content": response})
        
        return response
    

    def _explain_code(self, code: Optional[str]):
        prompt = f"Explain the following code in simple terms:\n{code}"
        self.chat_history.append({"role": "user", "content": prompt})

        messages = [{"role": "user", "content": prompt}]
        response = self._generate_response(role="user", message=messages)
        self.chat_history.append({"role": "assistant", "content": response})
        
        return response


    def process_query(self, query: str, code: Optional[str] = None):
        if code:
            user_prompt=f"Here is some code:\n{code}\nProvide assistance with the following query: {query}"
        else:
            user_prompt=query

        self.chat_history.append({"role": "user", "content": user_prompt})
        
        messages = self.chat_history
        response = self._generate_response(role="user", message=messages)
        self.chat_history.append({"role": "assistant", "content": response})
        
        return response
    

    def reset_chat(self):
        self.chat_history = [self._generate_system_prompt()]



    

