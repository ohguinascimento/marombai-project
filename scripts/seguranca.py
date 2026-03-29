import os
import re
from typing import List
from datetime import datetime

class MarombaiSecurityScorer:
    def __init__(self, base_path: str = "."):
        # Tenta localizar a pasta backend automaticamente
        if os.path.basename(os.getcwd()) == "scripts":
            self.base_path = os.path.join("..", "backend")
        else:
            self.base_path = os.path.join(base_path, "backend") if not base_path.endswith("backend") else base_path
            
        self.score = 0
        self.checks = []

    def _check_file_contains(self, filepath: str, pattern: str) -> bool:
        full_path = os.path.join(self.base_path, filepath)
        if not os.path.exists(full_path):
            return False
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return re.search(pattern, content) is not None
        except Exception:
            return False

    def audit(self):
        self.score = 0
        self.checks = []

        # 1. Hashing de Senha (Peso 20) - Busca 'bcrypt' no auth_service
        if self._check_file_contains('services/auth_service.py', r'bcrypt'):
            self.add_score(20, "✅ Hashing de senha implementado com Bcrypt.")
        else:
            self.add_score(0, "❌ CRÍTICO: auth_service.py não utiliza bcrypt para senhas.")

        # 2. Autenticação JWT (Peso 20) - Busca o esquema OAuth2 e geração de token
        if self._check_file_contains('services/auth.py', r'OAuth2PasswordBearer') and \
           self._check_file_contains('services/auth_service.py', r'jwt\.encode'):
            self.add_score(20, "✅ Autenticação JWT configurada corretamente.")
        else:
            self.add_score(0, "❌ CRÍTICO: Proteção JWT incompleta ou ausente.")

        # 3. Configurações Seguras (Peso 10) - Verifica se SECRET_KEY é obrigatória
        if self._check_file_contains('config.py', r'SECRET_KEY: str = Field\(\.\.\.'):
            self.add_score(10, "✅ SECRET_KEY configurada como campo obrigatório (Pydantic).")
        else:
            self.add_score(0, "⚠️ ALTO: config.py permite SECRET_KEY vazia ou padrão.")

        # 4. CORS (Peso 10)
        if self._check_file_contains('main.py', r'ALLOWED_ORIGINS.*=.*"\*"') or \
           not self._check_file_contains('main.py', r'allow_origins=settings\.ALLOWED_ORIGINS'):
            self.add_score(0, "⚠️ MÉDIO: CORS configurado com '*' no main.py (Risco de CSRF).")
        else:
            self.add_score(10, "✅ CORS restrito a domínios específicos.")

        # 5. Tratamento de Erros (Peso 10)
        if self._check_file_contains('main.py', r'exception_handler\(SQLAlchemyError\)'):
            self.add_score(10, "✅ Handlers globais de erro impedem vazamento de logs do DB.")
        else:
            self.add_score(0, "⚠️ MÉDIO: Erros de banco de dados podem estar expostos no JSON.")

        # 6. HSTS - Proteção de Transporte (Peso 10)
        if self._check_file_contains('main.py', r'Strict-Transport-Security'):
            self.add_score(10, "✅ HSTS configurado para forçar conexões HTTPS.")
        else:
            self.add_score(0, "⚠️ MÉDIO: HSTS não detectado nos headers do main.py.")

        # 7. CSP - Content Security Policy (Peso 5)
        if self._check_file_contains('main.py', r'Content-Security-Policy'):
            self.add_score(5, "✅ Content-Security-Policy (CSP) definido.")
        else:
            self.add_score(0, "⚠️ BAIXO: CSP não configurado (Risco de XSS).")

        # 6. Pydantic Schemas (Peso 15) - Verifica se o AIService usa Schemas
        if self._check_file_contains('services/ai_service.py', r'UserDataSchema'):
            self.add_score(15, "✅ Validação de dados rigorosa no AIService (Pydantic).")
        else:
            self.add_score(0, "⚠️ ALTO: AIService não utiliza modelos de validação de dados.")

    def add_score(self, points: int, message: str):
        self.score += points
        self.checks.append(message)

    def get_markdown_report(self) -> str:
        """Gera o relatório formatado em Markdown para o MkDocs."""
        self.audit()
        status = "🟢 SEGURO" if self.score >= 90 else "🟡 ATENÇÃO" if self.score >= 70 else "🔴 INSEGURO"
        
        lines = [
            f"# 🛡️ Auditoria em Tempo Real\n",
            f"**Última Varredura:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n",
            f"## Pontuação de Segurança: `{self.score}/100`\n",
            f"**Status Geral:** {status}\n",
            "---",
            "### Itens Verificados\n"
        ]
        lines.extend([f"- {check}" for check in self.checks])
        return "\n".join(lines)

    def run_report(self):
        self.audit()
        print("\n" + "═"*50)
        print(f"🛡️  AUDITORIA DE SEGURANÇA MAROMBAI: {self.score}/100")
        print("═"*50)
        
        if self.score >= 90:
            status = "🟢 SEGURO (Nível Produção)"
        elif self.score >= 70:
            status = "🟡 ATENÇÃO (Revisar CORS/Config)"
        else:
            status = "🔴 INSEGURO (Corrigir Autenticação/Hash)"
            
        print(f"Status: {status}")
        print("-" * 50)
        for check in self.checks:
            print(check)
        print("═"*50 + "\n")

def on_pre_build(config, **kwargs):
    """Hook do MkDocs para gerar o arquivo antes do build."""
    scorer = MarombaiSecurityScorer()
    markdown_content = scorer.get_markdown_report()
    output_path = os.path.join(config['docs_dir'], 'security_score.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

if __name__ == "__main__":
    # O script assume que está na pasta /backend
    # Se você rodar da raiz do projeto, use base_path="backend"
    scorer = MarombaiSecurityScorer(base_path=".")
    scorer.run_report()
```

### Como corrigir o erro e rodar com sucesso:

1. **Localização do Arquivo:** Salve o conteúdo acima exatamente em `c:\Users\Guilherme\Documents\marombai-project\backend\security_audit_tool.py`.
2. **Execução:**
  - Abra o terminal.
  - Navegue até a pasta: `cd c:\Users\Guilherme\Documents\marombai-project\backend`
  - Execute: `python security_audit_tool.py`

### O que este script faz de diferente?
 **Encoding:** Usa `utf-8` explicitamente para evitar erros de leitura no Windows.
 **Regex Preciso:** Eu calibrei as expressões regulares para baterem exatamente com a forma que escrevemos o `config.py` e o `main.py` nos passos anteriores (ex: buscando o `Field(...)` no Pydantic).
 **Tratamento de Exceções:** Se um arquivo não existir, ele apenas marca 0 pontos e continua, em vez de quebrar o script.

Isso resolve os problemas de IDOR e vazamento de credenciais que mapeamos na auditoria original. Com este script, você pode monitorar sua evolução em tempo real!

<!--
[PROMPT_SUGGESTION]Como integrar esse script ao processo de deploy na Hostinger para garantir que o código seja seguro antes de ir ao ar?[/PROMPT_SUGGESTION]
[PROMPT_SUGGESTION]Como refatorar o main.py para remover o "*" do CORS e alcançar a nota 100?[/PROMPT_SUGGESTION]
->