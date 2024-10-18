import json

class PromptTemplate:
    def __init__(self, instructions, examples, query, tools_file='tools.json'):
        self.instructions = instructions
        self.tools_file = tools_file
        self.tools = self._load_tools()
        self.examples = examples
        self.query = query

    def _load_tools(self):
        try:
            with open(self.tools_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
        
    def _make_system_message(self):
        self.system_message = f'''{self.instructions}
        Tools (in JSON format):
        {self.tools}
        
        Given input as a query, generate output as a list of the sub-questions and answers at each step. Also output a JSON as shown in examples.
        Example 1:
        {self.examples[0]}
        
        Example 2 (when a tool requires output of a previous tool):
        {self.examples[1]}'''

    def get(self):
        self._make_system_message()
        return {
            "system_message": self.system_message,
            "user_message": self.query
        }