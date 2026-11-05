import { createContext, useContext } from 'react'
import type { User } from 'firebase/auth'

export interface AuthContextValue {
  /** The signed-in user, or null when browsing anonymously. */
  user: User | null
  /** True until the first onAuthStateChanged callback fires. */
  loading: boolean
  signIn: (email: string, password: string) => Promise<void>
  signUp: (email: string, password: string) => Promise<void>
  signOut: () => Promise<void>
}

export const AuthContext = createContext<AuthContextValue | undefined>(undefined)

/** Read the current auth state. Must be called inside an <AuthProvider>. */
export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used inside an <AuthProvider>')
  }
  return context
}
