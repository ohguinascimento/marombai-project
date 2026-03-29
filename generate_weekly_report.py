import subprocess
import os
from datetime import datetime, timedelta

def get_weekly_commits():
    """Busca as mensagens de commit dos últimos 7 dias."""
    since_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    try:
        # Comando git para pegar commits sem merges
        cmd = [
            "git", "log", 
            f"--since={since_date}", 
            "--pretty=format:* %s (%h)",
            "--no-merges"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Erro ao buscar commits: {e}"

def generate_markdown_report(commits, truncate=False):
    """Formata o relatório no estilo MarombAI. Se truncate=True, limita para o Discord."""
    date_str = datetime.now().strftime('%d/%m/%Y')
    report = [
        f"# 🏋️‍♂️ MarombAI - Relatório de Progresso Semanal",
        f"**Data de extração:** {date_str}\n",
        "## 🚀 Alterações e Evoluções da Semana\n",
        commits if commits else "Nenhum commit encontrado nesta semana. *Foco no descanso também é treino!*",
        "\n---\n*Gerado automaticamente via GitHub Actions.*"
    ]
    report_text = "\n".join(report)

    if truncate:
        # Limite do Discord (2000 caracteres). Usamos 1900 por segurança.
        LIMIT = 1900
        if len(report_text) > LIMIT:
            warning = "\n\n⚠️ **Relatório truncado. Confira o log completo no repositório do GitHub.**"
            available_space = LIMIT - len(warning)
            truncated_text = report_text[:available_space]
            last_newline = truncated_text.rfind('\n')
            if last_newline != -1:
                truncated_text = truncated_text[:last_newline]
            report_text = truncated_text + warning

    return report_text

if __name__ == "__main__":
    commits_text = get_weekly_commits()
    
    # Gera versão completa
    full_report = generate_markdown_report(commits_text, truncate=False)
    with open("weekly_report_full.md", "w", encoding="utf-8") as f:
        f.write(full_report)
    
    # Gera versão para Discord
    discord_report = generate_markdown_report(commits_text, truncate=True)
    with open("weekly_report_discord.md", "w", encoding="utf-8") as f:
        f.write(discord_report)
        
    print("✅ Relatórios gerados: weekly_report_full.md e weekly_report_discord.md")