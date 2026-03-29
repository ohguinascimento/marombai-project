/**
 * MarombAI - Type Definitions
 * Sincronizado com backend/models.py
 */

export type UserRole = 'user' | 'admin';

export interface User {
  id: number;
  nome: string;
  email: string;
  idade: number;
  peso: number;
  altura: number;
  genero: 'masculino' | 'feminino';
  frequencia: number;
  local: string;
  objetivo: string;
  nivel: string;
  dieta?: string;
  role: UserRole;
  lesoes: string; // JSON string
  created_at: string;
}

export interface Exercicio {
  nome: string;
  series: string;
  carga: string;
  descanso?: string;
  dica_execucao?: string;
  img?: string;
}

export interface WorkoutPlan {
  id: number;
  titulo: string;
  foco: string;
  nivel_dificuldade: string;
  ai_insight: string;
  treino_json: string; // No banco é string
  exercicios?: Exercicio[]; // Quando processado pelo Backend
  created_at: string;
  user_id: number;
}

export interface WorkoutLog {
  id: number;
  user_id: number;
  workout_plan_id: number;
  data_realizacao: string;
  duracao_minutos: number;
  esforco_percebido: number;
  observacoes?: string;
  detalhes_json: string;
  exercicios?: Exercicio[]; // Mapeado no frontend
}

export interface DashboardData {
  user: User;
  treino: {
    titulo: string;
    foco: string;
    intensidade: string;
    ai_insight: string;
    exercicios: Exercicio[];
  } | null;
  treino_meta: WorkoutPlan | null;
  dieta: any | null; // Substituir por DietPlan interface quando definida
}