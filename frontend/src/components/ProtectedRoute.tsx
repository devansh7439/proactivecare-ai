import { ReactElement } from "react";
import { Navigate } from "react-router-dom";
import { tokenStore } from "../api/client";

interface ProtectedRouteProps {
  children: ReactElement;
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const token = tokenStore.getAccess();
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return children;
}
