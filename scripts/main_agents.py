import os
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
from crewai_tools import FileReadTool

# Carrega chaves de API (.env)
load_dotenv()

# Garante que o diretório de relatórios existe
os.makedirs('relatorios', exist_ok=True)

# Inicializa a ferramenta de leitura de arquivos (apenas leitura)
file_tool = FileReadTool()

# Configura o Gemini usando a classe nativa do CrewAI (LiteLLM)
# Isso resolve o erro de validação Pydantic no Python 3.13 e Pydantic v2
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")
gemini_llm = LLM(
    model="gemini/gemini-1.5-flash",
    temperature=0.2
)

# AGENTE 1: Treinador Master (Foco em Programação e Periodização)
treinador = Agent(
  role='Head Coach de Musculação',
  goal='Avaliar a seleção de exercícios e a divisão de treino (split) para máxima eficiência.',
  backstory='Treinador de atletas de elite com 20 anos de experiência em periodização linear e ondulatória.',
  llm=gemini_llm,
  verbose=True,
  tools=[file_tool]
)

# AGENTE 2: Fisiologista do Exercício (Foco em Volume e Intensidade)
fisiologista = Agent(
  role='Fisiologista do Exercício',
  goal='Analisar as variáveis de carga (séries, repetições, descanso) para garantir o estímulo metabólico correto.',
  backstory='Doutor em fisiologia humana, especialista em respostas hipertróficas e mecanismos de fadiga central.',
  llm=gemini_llm,
  verbose=True,
  tools=[file_tool]
)

# AGENTE 3: Especialista em Biomecânica (Foco em Segurança e Técnica)
biomecanico = Agent(
  role='Especialista em Cinesiologia e Biomecânica',
  goal='Validar a segurança das sequências de exercícios e prevenir riscos de lesão nos padrões recomendados.',
  backstory='Fisioterapeuta esportivo focado em análise de movimento e prevenção de lesões articulares.',
  llm=gemini_llm,
  verbose=True,
  tools=[file_tool]
)

# A TAREFA: O Debate
debate_task = Task(
  description="""Analise criticamente os treinos padrões (templates) definidos no arquivo 'backend/routers/workouts.py' 
  e a estrutura de dados de exercícios em 'backend/models.py'.
  
  1. O Treinador Master deve avaliar se os planos (Full Body, Push, Pull) seguem uma lógica de progressão lógica.
  2. O Fisiologista deve criticar as faixas de repetições (3x15 vs 4x10) e tempos de descanso para os objetivos propostos.
  3. O Especialista em Biomecânica deve alertar sobre possíveis sobrecargas articulares na ordem dos exercícios sugeridos.
  
  Recomendem melhorias para os templates atuais para torná-los 'Padrão Ouro' para os usuários do MarombAI.""",
  expected_output="""Um relatório técnico em Markdown contendo:
  1. Avaliação Crítica dos Templates Atuais (Adaptação, Push, Pull).
  2. Recomendações de Ajustes em Séries/Repetições/Descanso.
  3. Sugestão de Novos Templates Padrão (ex: Lower Body, Upper Body).
  4. Orientações de Segurança e Prevenção de Lesões baseadas na biomecânica.
  5. Resumo da análise científica para ser usado como 'AI Insight' no sistema.""",
  agent=treinador, # O treinador inicia
  output_file='relatorios/workout_expert_report.md'
)

# A Tripulação (Crew)
maromba_crew = Crew(
  agents=[treinador, fisiologista, biomecanico],
  tasks=[debate_task],
  process=Process.sequential,
  verbose=True
)

if __name__ == "__main__":
    print("🚀 Iniciando debate entre agentes IA...")
    result = maromba_crew.kickoff()
    print(f"✅ Debate concluído. Relatório gerado em: relatorios/workout_expert_report.md")