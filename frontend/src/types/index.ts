export interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T;
  errors?: unknown;
}

export interface Tokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in_seconds: number;
}

export interface UserProfile {
  id: number;
  email: string;
  age?: number;
  sex?: "male" | "female" | "other";
  height?: number;
  weight?: number;
  known_conditions?: string[];
  medications?: string[];
}

export interface HealthEntry {
  id: number;
  user_id: number;
  recorded_at: string;
  symptoms_text: string;
  symptom_tags: string[];
  heart_rate?: number;
  systolic_bp?: number;
  diastolic_bp?: number;
  temperature?: number;
  spo2?: number;
  glucose?: number;
  weight?: number;
  risk_score?: number;
  risk_level?: string;
}

export interface PredictionResult {
  symptom_tags: string[];
  predictions: { condition: string; confidence: number; recommended_next_steps: string[] }[];
  risk_score: number;
  risk_level: "Low" | "Moderate" | "High";
  emergency_warning: boolean;
  warning_message?: string;
  top_contributing_features: string[];
  disclaimer: string;
  entry_id?: number;
}
