import os
from datetime import datetime

def update_changelog(release_notes_path="monitoramento.md", changelog_path="CHANGELOG.md"):
    """
    Lê o conteúdo do arquivo de Release Notes e o insere como uma nova entrada
    no CHANGELOG.md, formatado com a data atual.
    """
    if not os.path.exists(release_notes_path):
        print(f"Erro: Arquivo de Release Notes não encontrado em '{release_notes_path}'")
        return

    with open(release_notes_path, 'r', encoding='utf-8') as f:
        release_notes_content = f.read()

    today_date = datetime.now().strftime("%Y-%m-%d")
    # Usamos uma versão fictícia por enquanto, mas em um fluxo real seria 0.1.0, 0.1.1, etc.
    new_entry_header = f"## [0.1.0] - {today_date}\n" # Ou a próxima versão semântica
    
    # Remove o cabeçalho existente do monitoramento.md para evitar duplicidade
    # e adiciona um cabeçalho de "Adicionado" para seguir o Keep a Changelog
    formatted_content = release_notes_content.replace("# 🚀 Notas de Lançamento (Release Notes)", "### Adicionado")

    # Lê o changelog existente, insere a nova entrada e salva
    with open(changelog_path, 'r+', encoding='utf-8') as f:
        content = f.read()
        # Evita duplicar se o script for rodado duas vezes no mesmo dia
        if new_entry_header in content:
            print("⚠️ Já existe uma entrada para a data de hoje.")
            return
        f.seek(0) # Volta para o início do arquivo
        f.write(new_entry_header + formatted_content + "\n\n" + content)
    
    print(f"✅ CHANGELOG.md atualizado com sucesso com as notas de '{release_notes_path}'")

if __name__ == "__main__":
    update_changelog()