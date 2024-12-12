from pydantic import BaseModel
from .base import Command, console

"""
INPUT - informar path do arquivo
LER O ARQUIVO
ENVIAR O CONTEUDO DO ARQUIVO COM O SYSTEM PROMPT PARA O AGENTE
RECEBER O GUIDELINE
SALVAR O GUIDELINE NO ARQUIVO
"""

system_prompt = """
You are a guideline assistant.
Given a file content, you will provide a guideline for the file.
The guideline should be a list of rules that the file should follow.
The guideline must be in markdown format.
The guideline can use mermaid diagrams to represent the file structure, if necessary.
FILE CONTENT:
"""

class GuidelineResult(BaseModel):
    guideline: str

class GenerateGuidelineCommand(Command):
    def __init__(self):
        super().__init__(
            name="generate-guideline",
            help="Generate a guideline from a file"
        )
    
    def execute(self, file_path: str, *args, **kwargs) -> None:
        file_content = self._read_file(file_path)
        console.print("File content loaded.")
        guideline = self._generate_guideline(file_content)
        console.print("Guideline generated.")
        self._save_guideline(guideline, file_path)
        console.print("Guideline saved.")

    def _read_file(self, file_path: str) -> str:
        with open(file_path, 'r') as file:
            return file.read()

    def _generate_guideline(self, file_content: str) -> str:
        result = self.agent.run_sync(system_prompt, file_content)
        return result.data.guideline

    def _save_guideline(self, guideline: str, file_path: str) -> None:
        with open(file_path+'.guideline.md', 'w') as file:
            file.write(guideline)
