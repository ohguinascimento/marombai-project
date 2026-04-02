import os
import re
from pathlib import Path

def estabilizar_projeto(root_dir: str):
    """
    Varre o projeto e corrige automaticamente referências obsoletas
    garantindo a consistência entre UserAuth e UserProfile.
    """
    # Mapeamento de padrões para substituição
    # \b garante que o Regex procure pela palavra exata
    replacements = {
        # 0. Limpa mutações erradas de execuções anteriores
        r'\bUserAuthAuth\b': 'UserAuth',
        r'\bUserAuthProfile\b': 'UserProfile',
        
        # 1. Corrige a classe User isolada para UserAuth (apenas se for a palavra exata)
        r'(?<!UserAuth)(?<!UserProfile)\bUser\b(?!Auth)(?!Profile)': 'UserAuth',
        
        # 2. Corrige strings de chaves estrangeiras e erros de banco
        r'"user\.email"': '"userauth.email"',
        r"'user\.email'": "'userauth.email'",
        r'foreign_key="user\.id"': 'foreign_key="userauth.id"',
        
        # 3. Garante que imports de models incluam UserAuth
        r'from backend\.models import (.*)\bUser\b(?!Auth)(?!Profile)(.*)': r'from backend.models import \1UserAuth\2',
    }

    ignored_dirs = {'.venv', 'venv', '__pycache__', '.git', 'node_modules', 'dist', 'htmlcov'}
    
    print(f"🔍 Iniciando estabilização em: {root_dir}")
    total_fixed = 0

    for root, dirs, files in os.walk(root_dir):
        # Filtra diretórios ignorados
        dirs[:] = [d for d in dirs if d not in ignored_dirs]

        for file in files:
            if not file.endswith('.py'):
                continue
            
            file_path = Path(root) / file
            # Não deixa o script se auto-editar
            if file == 'estabilizar_projeto.py':
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                new_content = content
                for pattern, subst in replacements.items():
                    new_content = re.sub(pattern, subst, new_content)

                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"✅ Estabilizado: {file_path}")
                    total_fixed += 1
            except Exception as e:
                print(f"❌ Falha ao processar {file_path}: {e}")

    print(f"\n✨ Sucesso! {total_fixed} arquivos foram corrigidos e o projeto deve subir agora.")

if __name__ == "__main__":
    # Define a raiz do projeto (um nível acima da pasta scripts)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    estabilizar_projeto(project_root)